from .views import *


class RequestList(View):
    template_name = 'homepage/request-list.html'

    def get(self, request):
        request_record = InspectionRequest.objects.get(pk=request.GET.get('request_id'))
        return render(request, self.template_name, {'record': request_record})
