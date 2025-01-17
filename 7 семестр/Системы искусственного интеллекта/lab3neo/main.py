from neo4j import GraphDatabase
import numpy as np

class StorageControlSystem:
    def __init__(self, uri, user, password):  # Инициализация драйвера для подключения к Neo4j
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Метод для получения действия на основе текущих условий
    def get_action(self, temperature, humidity):
        # Фаззификация температуры и влажности
        temp_condition = self.fuzzify_temperature(temperature)
        hum_condition = self.fuzzify_humidity(humidity)

        # Запрос к Neo4j
        query = (
            "MATCH (temp:Condition {value: $temp_condition})-[temp_action:ACTION]->(temp_next:Condition), "
            "(hum:Condition {value: $hum_condition})-[hum_action:ACTION]->(hum_next:Condition) "
            "RETURN temp_action.name AS temp_action, hum_action.name AS hum_action "
            "LIMIT 1"
        )

        with self.driver.session() as session:
            result = session.run(query, temp_condition=temp_condition, hum_condition=hum_condition)
            actions = result.single()
            if actions:
                return actions["temp_action"], actions["hum_action"]
            return None, None

    # Фаззификация температуры
    def fuzzify_temperature(self, temperature):
        if temperature < 15:
            return "Cold"
        elif 15 <= temperature <= 25:
            return "Optimal"
        else:
            return "Hot"

    # Фаззификация влажности
    def fuzzify_humidity(self, humidity):
        if humidity < 30:
            return "Dry"
        elif 30 <= humidity <= 60:
            return "Optimal"
        else:
            return "Humid"

    # Метод симуляции
    def simulate(self, initial_temperature, initial_humidity, steps=10):
        temperature = initial_temperature
        humidity = initial_humidity

        for step in range(steps):
            # Получаем действия из Neo4j
            temp_action, hum_action = self.get_action(temperature, humidity)

            # Адаптация температуры
            if temp_action == "IncreaseTemperature":
                temperature += np.random.uniform(1, 3)
            elif temp_action == "DecreaseTemperature":
                temperature -= np.random.uniform(1, 3)

            # Адаптация влажности
            if hum_action == "IncreaseHumidity":
                humidity += np.random.uniform(5, 10)
            elif hum_action == "DecreaseHumidity":
                humidity -= np.random.uniform(5, 10)

            # Поддержание значения в пределах допустимого диапазона
            temperature = max(0, round(temperature, 2))
            humidity = max(0, round(humidity, 2))

            # Вывод текущего состояния
            print(f"Step {step}: Temperature={temperature}, Humidity={humidity}, TempAction={temp_action}, HumAction={hum_action}")

# Запуск симуляции
if __name__ == "__main__":
    uri = "neo4j+s://aaf5a1c2.databases.neo4j.io"
    user = "neo4j"
    password = "XR7syNnjzjKhXVccWJyko_CzFVlYZDsD_KmTswf3bkk"

    system = StorageControlSystem(uri, user, password)

    try:
        system.simulate(initial_temperature=10, initial_humidity=20, steps=10)
    finally:
        system.close()
