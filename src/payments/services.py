from django.core.paginator import Page


class RequisiteService:
    def get_ajax_response(self, context):
        page_obj: Page = context['page_obj']
        response_data = {
            'object_list': page_obj.object_list,
            'page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previos': page_obj.has_previous(),
            'has_other_pages': page_obj.has_other_pages(),
            'num_pages': page_obj.paginator.num_pages,
        }
        return response_data
