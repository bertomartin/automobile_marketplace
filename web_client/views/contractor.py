from .views import *


class RequestList(View):
    template_name = 'homepage/workshop/request-list.html'

    def get(self, request):
        request_record = InspectionRequest.objects.get(pk=request.GET.get('request_id'))
        return render(request, self.template_name, {'record': request_record})


class TabContent(View):
    template_name = 'homepage/workshop/tab_content.html'

    def get(self, request):
        record = InspectionRequest.objects.get(pk=request.GET.get('request_id'))
        form = EditInspectionForm(instance=InspectionRequest.objects.get(pk=request.GET.get('request_id')))
        return render(request, self.template_name, {'form':form, 'record': record})
