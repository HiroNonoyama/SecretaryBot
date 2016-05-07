# coding: utf-8

# changing the structure type of json data, classifying the type of user' input command and connecting to batabase
class MessageHandler:

    def __init__(self, message, user_id):
        self.message = message["message"]
        self.user_id = user_id
        self.message_array = self.message.split("\n")

        switch = {
        u"登録": "create",
        u"削除": "delete",
        u"表示": "show"
        }
        method_name = unicode(self.message_array[0], "utf-8")
        self.method = switch[method_name]

        method_array = [u"登録", u"削除", u"表示"]
        if not method_name in method_array:
            self.method = "etc"


    def create(self):
        message_array = self.message_array
        message_array.extend(["", "", ""])
        # add the empty element (because prevent "index of out range" with message_array[3or2or1])
        return {
            "method": "create",
            "user_id": self.user_id,
            "data": {
              "date": message_array[1],
              "title": message_array[2],
              "description": message_array[3]
            }
        }

    def delete(self):
        message_array = self.message_array
        message_array.append("")
        # add the empty element
        return {
            "method": "delete",
            "user_id": self.user_id,
            "data": {
                "id": message_array[1]
            }
        }

    def show(self):
        return {
            "method": "show",
            "user_id": self.user_id
        }

    def excute(self):

        switch = {
            "create": self.create(),
            "delete": self.delete(),
            "show": self.show(),
            "etc": {"method": "etc", "user_id": self.user_id}
        }

        return switch[self.method]

