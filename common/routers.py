# class ScrapedDataRouter:
#     route_app_labels = {'data'}
#
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return 'scraped_data'
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return 'scraped_data'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         if (
#                 obj1._meta.app_label in self.route_app_labels or
#                 obj2._meta.app_label in self.route_app_labels
#         ):
#             return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label in self.route_app_labels:
#             return db == 'scraped_data'
#         return None


class CheckerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'data':
            return 'contentdb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'data':
            return 'contentdb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in chinook app"
        if obj1._meta.app_label == 'data' and obj2._meta.app_label == 'data':
            return True
        # Allow if neither is chinook app
        elif 'data' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'data':
            return db == 'contentdb'
        elif app_label == 'chat':
            return db == 'default'
        return None