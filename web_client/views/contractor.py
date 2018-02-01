from .views import *


class RequestList(View):
    template_name = 'homepage/request-list.html'

    def get(self, request):
        request_record = InspectionRequest.objects.get(pk=request.GET.get('request_id'))
        return render(request, self.template_name, {'record': request_record})


class TabContent(View):
    template_name = 'homepage/tab_content.html'

    def get(self, request):
        # TODO create Inspection form to be passed to this template
        record = InspectionRequest.objects.get(pk=request.GET.get('request_id'))
        return render(request, self.template_name, {'record': record})
