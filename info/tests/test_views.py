from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from info.models import Category, DetailInfo


class TestInfoViews(TestCase):

    def setUp(self):
        """Sets up a HomeCarousel model."""
        image = SimpleUploadedFile(
            name='default.jpg',
            content=open(
                'media/default.jpg',
                'rb').read(),
            content_type='image/jpeg',)

        valid_category = Category(title_en='HI1',
                                  title_it='HI1',
                                  menu_word_en='HCMW1',
                                  menu_word_it='HCMW1',
                                  description_en='description',
                                  description_it='description',
                                  image=image,
                                  button_text="text here",
                                  order=1)
        valid_category.save()

        valid_detailinfo = DetailInfo(
            category=Category.objects.latest('date_added'),
            title_en='HI1',
            title_it='HI1',
            summary_en='HCMW1',
            summary_it='HCMW1',
            desc_title1_en='heading',
            desc_title1_it='heading',
            description1_en='description',
            description1_it='description',
            title_image=image,
            desc_image=image,
            theme='brown',
            order=1)
        valid_detailinfo.save()

    def test_render_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/index.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')

    def test_render_category_detail(self):
        category = Category.objects.latest('date_added')
        response = self.client.get(f'/category/{category.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/category_detail.html')
        self.assertTemplateUsed(response, 'info/includes/category_info.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(response.context['active_category'], f'{category.id}')
        self.assertTrue(response.context['active_all'], f'{category.id}')

    def test_render_info_detail(self):
        detailinfo = DetailInfo.objects.latest('date_added')
        response = self.client.get(f'/detailinfo/{detailinfo.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/detailinfo_detail.html')
        self.assertTemplateUsed(response, 'base/base.html')
        self.assertTemplateUsed(response, 'base/includes/header.html')
        self.assertTemplateUsed(response, 'base/includes/footer.html')
        self.assertTrue(
            response.context['active_category'], f'{detailinfo.id}')
        self.assertTrue(response.context['active_page'], f'{detailinfo.id}')
