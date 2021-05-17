"""
Definition of the :class:`MeasurementDefinitionSerializer` class.
"""

from research.models.measurement_definition import MeasurementDefinition
from rest_framework import serializers


class MeasurementDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.measurement_definition.MeasurementDefinition`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    class Meta:
        model = MeasurementDefinition
        fields = "id", "title", "description"
