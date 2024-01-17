import csv

from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset, field_names=None):
        meta = self.model._meta
        if not field_names:
            field_names = [field.name for field in meta.fields]
            print(field_names)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row_data = []
            for field in field_names:
                if '__' not in field:
                    row_data.append(getattr(obj, field))
                else:
                    field = field.split('__')
                    row_data.append(getattr(getattr(obj, field[0]), field[1]))

            row = writer.writerow(row_data)

        return response
