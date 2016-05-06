# coding: utf-8
# coding=utf-8

# changing the structure type of json data, classifying the type of user' input command and connecting to batabase
class MessageHundler:

	def __init__(self, message, user_id):
		self.message = message["message"]
		self.user_id = user_id
		self.message_array = self.message.split("\n")

	# classyfing the type of command
	def classify_method(self):

		switch = {
		u"登録": "create",
		u"削除": "delete",
		u"表示": "show"
		}
		message_array = self.message.split("\n")
		method_name = unicode(message_array[0], "utf-8")

		if method_name != u"登録" and method_name != u"削除" and method_name != u"表示":
			method_name = "etc"
			return "etc"

		return switch[method_name]

	# changing the structure of json data
	def change_data_structure(self, method):

		def data_to_create(self):
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

		def data_to_delete(self):
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

		def data_to_show(self):
			return {
				"method": "show",
				"user_id": self.user_id
			}

		switch = {
			"create": data_to_create(self),
			"delete": data_to_delete(self),
			"show": data_to_show(self),
			"etc": {"method":"etc", "user_id": self.user_id}
		}
		print switch[method]


	def excute(self):
		self.change_data_structure(self.classify_method())


message1 = MessageHundler({"message":"登録\n5/7\n読書\n村上春樹を読む"}, 1374570)
message2 = MessageHundler({"message":"削除\n5"}, 32431123)
message3 = MessageHundler({"message":"表示"}, 14653123)
message4 = MessageHundler({"message":"変更"}, 34712740)
message1.excute()
message2.excute()
message3.excute()
message4.excute()
