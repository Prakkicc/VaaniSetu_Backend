from rest_framework import serializers

class TextProcessSerializer(serializers.Serializer):
    # We now expect a 'text' field from the other backend
    text = serializers.CharField(required=True, allow_blank=False)

    def validate_text(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Text content is too short to process.")
        return value