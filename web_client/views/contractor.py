from .views import *


class RequestList(View):
    template_name = 'homepage/workshop/request-list.html'

    def get(self, request):
        request_record = InspectionRequest.objects.get(pk=request.GET.get('request_id'))
        return render(request, self.template_name, {'record': request_record})


class RequestEvaluationContainer(View):

    def get(self, request):
        return render(request, 'homepage/workshop/tab_content.html', {'request_id': request.GET.get('request_id')})


class RequestEvaluation(View):
    template_name = 'homepage/workshop/request-evaluation-form.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        form = EditInspectionForm(instance=InspectionRequest.objects.get(pk=id))
        return render(request, self.template_name, {'form': form, 'record': id})

    def post(self, request, *args, **kwargs):
        form = EditInspectionForm(data=request.POST, instance=InspectionRequest.objects.get(pk=self.kwargs['id']))
        if form.is_valid():
            form.save()
            form = EditInspectionForm(instance=InspectionRequest.objects.get(pk=self.kwargs['id']))

        return render(request, self.template_name, {'form': form})
