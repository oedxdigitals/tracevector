import re
class EmailPlugin:
    name = "email"

    def run(self, target):
        return {
            "target": target,
            "disposable_email": False
        }
