from dbcontroller.models import Subscriber, Owner


class ModelsFactory:
    subscriber = Subscriber
    owner = Owner

    def init(self):
        self.subscriber.create_table(safe=True)
        self.owner.create_table(safe=True)