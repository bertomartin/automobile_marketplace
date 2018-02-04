from .views import *


@method_decorator([login_required], name='dispatch')
class CreatePost(View):
    template_name = 'post/edit_post.html'

    def get(self, request):
        form = OfferForm(initial={'contact_person': Customer.objects.get(user_id=request.user).name})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OfferForm(self.request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('homepage')

        return render(request, self.template_name, {'form': form})


@method_decorator([login_required], name='dispatch')
class SeriesPicklist(View):
    template_name = 'post/series_list_options.html'

    def get(self, request):
        manufacturer_id = request.GET.get('manufacturer_id')
        series = Series.objects.filter(make_fk=manufacturer_id).order_by('series')
        return render(request, self.template_name, {'series': series})


@method_decorator([login_required], name='dispatch')
class UploadImages(View):
    template_name = 'post/image_upload.html'

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        images = Image.objects.filter(post_id=post_id)
        return render(self.request, self.template_name, {'photos': images})

    def post(self, request):
        form = ImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


@method_decorator([login_required], name='dispatch')
class UserPosts(View):
    template_name = 'homepage/customer/user_offers.html'

    def get(self, request):
        posts = Post.objects.filter(owner=request.user)
        return render(request, self.template_name, {'offers': posts})


class WorkshopsList(View):
    template_name = 'homepage/customer/workshops_modal.html'

    def get(self, request):
        post_id = request.GET.get('post_id')
        workshops = Contractor.objects.filter(status=True)

        return render(request, self.template_name, {'post': Post.objects.get(pk=post_id), 'contractors': workshops})


def request_inspection(request):
    contractor = Contractor.objects.get(user_id=request.GET.get('contractor_id'))
    post = Post.objects.get(offer_id=request.GET.get('post_id'))
    customer = Customer.objects.get(user=request.user)

    try:
        if InspectionRequest.objects.filter(corresponding_post=post,
                                            responsible_contractor=contractor,
                                            requesting_customer=customer).count() > 0:
            message = 'This request request already exists for this user.'
            status = False
        else:
            inspection = InspectionRequest(corresponding_post=post,
                                           responsible_contractor=contractor,
                                           requesting_customer=customer)
            inspection.save()
            message = 'Your request to {} was successfully created.'.format(contractor.title)
            status = True
    except Exception as e:
        message = 'Something went wrong during this request.'
        status = False
        print('Couldn\'t create inspection request: \n', e)

    return JsonResponse({'message': message, 'status': status})
