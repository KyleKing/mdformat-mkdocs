# Testing #13

1. Add a serializer class

    ```python
    class RecurringEventSerializer(serializers.ModelSerializer):  # (1)!
        """Used to retrieve recurring_event info"""


    class Meta:
        model = RecurringEvent  # (2)!
        fields = (
            "uuid",
            "name",
            "start_time",
            "duration_in_min",
            "video_conference_url",
            "additional_info",
            "project",
        )
        read_only_fields = (
            "uuid",  # (3)!
            "created_at",
            "updated_at",
        )
    ```
