"""Core Python and classes exercise using the adjacent employees.csv file."""
import csv
from functools import wraps
from pathlib import Path
from typing import Any, Callable


def calculate_bonus(
    salary: float,
    rate: float = 0.1,
    *extras: float,
    **options: Any,
) -> float:
    """Return salary times rate plus extras, optionally limited by a cap."""
    bonus = salary * rate + sum(extras)
    if "cap" in options:
        bonus = min(bonus, options["cap"])
    return bonus


class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary

    def get_details(self) -> str:
        return f"{self.name} - ${salary}:,.2f}"

    @property
    def annual_salary(self) -> float:
        return self.salary * 12


def log_call(fun: Callable[..., Any]) -> Callable[..., Any]:
    """Print the function name before calling it."""
    @wraps(fun)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {fun.__name__}")
        return fun(*args, **kwargs)

    return wrapper


class Manager(Employee):
    def __init__(self, name: str, salary: float, team_size: int) -> None:
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self) -> str:
        return f"{super().get_details()} - Team size: {self.team_size}"

    @staticmethod
    def salary_category(salary: float) -> str:
        if salary < 50_000:
            return "Low"
        if salary < 70_000:
            return "Medium"
        return "High"


def main() -> None:
    csv_path = Path(__file__).with_name("employees.csv")
    if csv_path.exists():
        with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                employee = Employee(row["name"], float(row["salary"]))
                category = Manager.salary_category(employee.salary)
                print(f"{employee.name} - {category} salary")
    else:
        print(f"Employee data file not found: {csv_path}")

    manager = Manager("Divya", 75_000, team_size=5)
    print(manager.get_details())


if __name__ == "__main__":
    main()
