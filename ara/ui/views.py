import codecs

from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from ara.api import filters, models, serializers
from ara.ui import forms


class Index(generics.ListAPIView):
    """
    Returns a list of playbook summaries
    """

    queryset = models.Playbook.objects.all()
    filterset_class = filters.PlaybookFilter
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        # TODO: Can we retrieve those fields automatically ?
        fields = ["order", "name", "started_after", "status"]
        search_query = False
        for field in fields:
            if field in request.GET:
                search_query = True

        if search_query:
            search_form = forms.PlaybookSearchForm(request.GET)
        else:
            search_form = forms.PlaybookSearchForm()

        serializer = serializers.ListPlaybookSerializer(self.filter_queryset(self.queryset.all()), many=True)
        return Response(
            {"page": "index", "playbooks": serializer.data, "search_form": search_form, "search_query": search_query}
        )


class Playbook(generics.RetrieveAPIView):
    """
    Returns a page for a detailed view of a playbook
    """

    queryset = models.Playbook.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "playbook.html"

    def get(self, request, *args, **kwargs):
        playbook = self.get_object()
        serializer = serializers.DetailedPlaybookSerializer(playbook)
        return Response({"playbook": serializer.data})


class Host(generics.RetrieveAPIView):
    """
    Returns a page for a detailed view of a host
    """

    queryset = models.Host.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "host.html"

    def get(self, request, *args, **kwargs):
        host = self.get_object()
        serializer = serializers.DetailedHostSerializer(host)
        return Response({"host": serializer.data})


class File(generics.RetrieveAPIView):
    """
    Returns a page for a detailed view of a file
    """

    queryset = models.File.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "file.html"

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        serializer = serializers.DetailedFileSerializer(file)
        return Response({"file": serializer.data})


class Result(generics.RetrieveAPIView):
    """
    Returns a page for a detailed view of a result
    """

    queryset = models.Result.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "result.html"

    def get(self, request, *args, **kwargs):
        # Results can contain a wide array of non-ascii or binary characters, escape them
        codecs.register_error("strict", codecs.lookup_error("surrogateescape"))
        result = self.get_object()
        serializer = serializers.DetailedResultSerializer(result)
        return Response({"result": serializer.data})


class Record(generics.RetrieveAPIView):
    """
    Returns a page for a detailed view of a record
    """

    queryset = models.Record.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "record.html"

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = serializers.DetailedRecordSerializer(record)
        return Response({"record": serializer.data})
