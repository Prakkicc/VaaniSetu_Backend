from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .apps import NlpEngineConfig
from .serializers import TextProcessSerializer
from .nlp_utils import predict_intent_backend
# Ensure mastersheet.py is in the core_logic folder
from core_logic.mastersheet import get_required_entities 

class ProcessTextView(APIView):
    """
    API Endpoint that returns a structured object containing 
    the predicted intent and the required entities.
    """
    def post(self, request):
        # 1. Validate that the caller sent a 'text' field
        serializer = TextProcessSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_text = serializer.validated_data['text']

        try:
            # 2. Check if the trained intent model is loaded
            model = NlpEngineConfig.model
            if model is None:
                return Response(
                    {"error": "NLP Intent Model is not initialized on the server."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 3. Use the smart-splitter logic to find intents
            intents_found = predict_intent_backend(user_text, model)
            
            # 4. Extract the primary action intent
            primary_intent = "OUT_OF_SCOPE"
            if intents_found:
                # Prioritize 'QUERY' or 'OPEN' tags over greetings
                query_intents = [i for i in intents_found if "QUERY" in i or "OPEN" in i]
                primary_intent = query_intents[0] if query_intents else intents_found[0]

            # 5. Fetch the mandatory entities from the mastersheet
            required_entities = get_required_entities(primary_intent)

            # 6. Return the final JSON object to the caller
            return Response({
                "status": "success",
                "intent_data": {
                    "primary_intent": primary_intent,
                    "all_detected_intents": intents_found,
                    "required_entities": required_entities
                },
                "input_processed": user_text
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)