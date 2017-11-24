from mvc.model.model import Model
from mvc.view.view import View
from mvc.controller.controller import Controller


def main():
	model = Model()
	model.add_player()
	view = View(model)
	controller = Controller(model, view)
	view.run()
	controller.run()


if __name__ == "__main__":
	main()
