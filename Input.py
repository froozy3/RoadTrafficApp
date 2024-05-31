from enum import Enum
import json
import random
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CargoType(Enum):
    allowed = 'allowed'
    permission_required = 'permission_required'
    banned = 'banned'


class TransportType(Enum):
    car = 'car'
    truck = 'truck'


class Cargo:
    def __init__(self, probability: float, type: CargoType, name: str):
        self.probability = probability
        self.type = type
        self.name = name

    @staticmethod
    def from_json(json_data):
        return Cargo(float(json_data['probability']), CargoType(json_data['type']), str(json_data['name']))

    def __str__(self):
        return (f"Cargo:"
                f"probability: {self.probability} "
                f"type: {self.type} "
                f"name: {self.name}")


class Colors:
    def __init__(self, allowed, banned, banned_probability: float):
        self.allowed = allowed
        self.banned = banned
        self.banned_probability = banned_probability

    def __str__(self):
        return (f"Colors:"
                f"allowed: {self.allowed} "
                f"banned: {self.banned} "
                f"banned_probability: {self.banned_probability}")

    @staticmethod
    def from_json(json_data):
        if json_data is not None:
            allowed = list[str](json_data['allowed_colors'])
            banned = list[str](json_data['banned_colors'])
            banned_probability = float(json_data['banned_probability'])
            return Colors(allowed, banned, banned_probability)
        else:
            return None


class Direction:
    def __init__(self, right, wrong):
        self.right = right
        self.wrong = wrong

    def __str__(self):
        return (f"Direction:"
                f"right: {self.right} "
                f"wrong: {self.wrong}")

    @staticmethod
    def from_json(json_data):
        return Direction(float(json_data['right']), float(json_data['wrong']))


class EngineType(Enum):
    hybrid = 'hybrid'
    gas = 'gas'
    electric = 'electric'
    gasoline = 'gasoline'


class Engine:
    def __init__(self, type: EngineType, probability: float):
        self.type = type
        self.probability = probability

    def __str__(self):
        return (f"Engine:"
                f"type: {self.type} "
                f"probability: {self.probability}")

    @staticmethod
    def from_json(json_data):
        return Engine(EngineType(json_data['type']), float(json_data['probability']))


class Speed:
    def __init__(self, max, min, probability: float):
        self.max = max
        self.min = min
        self.probability = probability

    def __str__(self):
        return (f"Speed:"
                f"max: {self.max} "
                f"min: {self.min} "
                f"probability: {self.probability}")

    @staticmethod
    def from_json(json_data):
        return Speed(int(json_data['max']), int(json_data['min']), float(json_data['probability']))


class Transport:
    def __init__(self, type: TransportType, weight: int, color: str, engine: str, cargo_permission: bool, cargo: str,
                 speed: int, is_direction_right: bool):
        self.type = type
        self.weight = weight
        self.color = color
        self.engine = engine
        self.cargo_permission = cargo_permission
        self.cargo = cargo
        self.speed = speed
        self.is_direction_right = is_direction_right

    def __str__(self):
        return (f"Transport instance:"
                f"\nType: {self.type}"
                f"\nWeight: {self.weight}"
                f"\nColor: {self.color}"
                f"\nEngine: {self.engine}"
                f"\nCargo_permission: {self.cargo_permission}"
                f"\nCargo: {self.cargo}"
                f"\nSpeed: {self.speed}"
                f"\nDirection: {self.is_direction_right}"
                f"\n-------------------"
                )


class TransportDescriptionProbabilities:
    def __init__(self, type_desc, weight, colors, engine, cargo_permission_availability, cargo, speed, direction):
        self.type = type_desc
        self.weight = weight
        self.colors = colors
        self.engine = engine
        self.cargo_permission_availability = cargo_permission_availability
        self.cargo = cargo
        self.speed = speed
        self.direction = direction

    def __str__(self):
        return (f"TransportDescriptionProbabilities:"
                f"Type: {self.type} "
                f"Weight: {self.weight} "
                f"Colors: {self.colors} "
                f"Engine: {self.engine} "
                f"Cargo_permission: {self.cargo_permission_availability} "
                f"Cargo: {self.cargo} "
                f"Speed: {self.speed} "
                f"Direction: {self.direction}")

    @staticmethod
    def from_json(json_data):
        # create list data from json
        type_desc = [TransportTypeDescription.from_json(t) for t in json_data["types"]]
        weight = [Weight.from_json(w) for w in json_data["weights"]]
        colors = Colors.from_json(json_data["colors"])
        engine = [Engine.from_json(e) for e in json_data["engines"]]
        cargo_permission_availability = float(json_data["cargo_permission_availability"])
        cargo = [Cargo.from_json(c) for c in json_data["cargos"]]
        speed = [Speed.from_json(s) for s in json_data["speeds"]]
        direction = Direction.from_json(json_data["directions"])

        return TransportDescriptionProbabilities(type_desc, weight, colors, engine,
                                                 cargo_permission_availability,
                                                 cargo, speed, direction)


class TransportTypeDescription:
    def __init__(self, type: TransportType, probability: float):
        self.type = type
        self.probability = probability

    def __str__(self):
        return (f"TransportTypeDescription:"
                f"Type: {self.type} "
                f"Probability: {self.probability}")

    @staticmethod
    def from_json(json_data):
        return TransportTypeDescription(TransportType(json_data["name"]), float(json_data["probability"]))


class Weight:
    def __init__(self, max, min, probability: float):
        self.max = max
        self.min = min
        self.probability = probability

    def __str__(self):
        return (f"Weight:"
                f"max: {self.max} "
                f"min: {self.min} "
                f"probability: {self.probability}")

    @staticmethod
    def from_json(json_data):
        return Weight(int(json_data['max']), int(json_data['min']), float(json_data['probability']))


class TransportGenerator:
    @staticmethod
    def generate_from(probabilities: TransportDescriptionProbabilities):
        if probabilities is None:
            logging.error("Probabilities cannot be None")
        # generate random values
        transport_type = TransportGenerator.randomize_for_types(probabilities.type)
        weight = TransportGenerator.randomize_for_weight(probabilities.weight)
        color = TransportGenerator.randomize_for_colors(probabilities.colors)
        engine = TransportGenerator.randomize_for_engines(probabilities.engine)
        cargo_permission = TransportGenerator.randomize_for_cargo_permission(
            probabilities.cargo_permission_availability)
        cargo = TransportGenerator.randomize_for_cargos(probabilities.cargo)
        speed = TransportGenerator.get_random_speed(probabilities.speed)
        direction = TransportGenerator.randomize_for_right_direction(probabilities.direction)
        transport = Transport(transport_type, weight, color, engine, cargo_permission, cargo, speed, direction)
        return transport

    @staticmethod
    def randomize(engines):
        return random.choice(engines)

    @staticmethod
    def randomize_for_cargos(cargos):
        cargo_choose = random.choice(cargos)
        return cargo_choose.name

    @staticmethod
    def randomize_for_right_direction(direction):
        probability = random.random()
        return probability < direction.right

    @staticmethod
    def randomize_for_cargo_permission(cargo_permission_availability):
        probability = random.random()
        return probability < cargo_permission_availability

    @staticmethod
    def randomize_for_weight(weights):
        total_probability = sum(w.probability for w in weights)
        random_value = random.random() * total_probability
        cumulative_probability = 0
        for weight in weights:
            cumulative_probability += weight.probability
            if random_value <= cumulative_probability:
                max_weight = weight.max
                if max_weight is not None:
                    return random.randint(weight.min, max_weight)
                else:
                    return weight.min

    @staticmethod
    def randomize_for_types(types):
        return random.choice(types).type.value

    @staticmethod
    def get_random_speed(speeds):
        probability = random.random()
        cumulative_probability = 0
        for speed in speeds:
            cumulative_probability += speed.probability
        if probability <= cumulative_probability:
            return random.randint(speed.min, speed.max)
        return 0

    @staticmethod
    def randomize_for_colors(colors):
        total_probability = sum(colors.banned_probability for _ in colors.banned)
        total_probability += sum(1.0 - colors.banned_probability for _ in colors.allowed)
        random_value = random.random() * total_probability
        cumulative_probability = 0

        for color in colors.banned:
            cumulative_probability += colors.banned_probability
            if random_value <= cumulative_probability:
                return color

        for color in colors.allowed:
            cumulative_probability += 1.0 - colors.banned_probability
            if random_value <= cumulative_probability:
                return color

        return None

    @staticmethod
    def randomize_for_engines(engines):
        total_probability = sum(engine.probability for engine in engines)
        random_value = random.random() * total_probability
        cumulative_probability = 0

        for engine in engines:
            cumulative_probability += engine.probability
            if random_value <= cumulative_probability:
                return engine.type.value
        return None


def main():
    data_json = load_json("probability_table.json")
    probabilities = TransportDescriptionProbabilities.from_json(data_json)
    for i in range(10):
        transport = TransportGenerator.generate_from(probabilities)
        print(transport)


def load_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
        logging.debug(f"Loaded JSON data: {data}")
        return data


if __name__ == "__main__":
    main()
