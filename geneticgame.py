from mvc.controller.controller import Controller
from mvc.model.model import Model
from mvc.view.view import View


def main():
    model = Model()
    model.create_terrain()
    model.add_player()
    model.add_player()
    view = View(model)
    controller = Controller(model, view)
    view.run()
    controller.run()


if __name__ == "__main__":
    main()
