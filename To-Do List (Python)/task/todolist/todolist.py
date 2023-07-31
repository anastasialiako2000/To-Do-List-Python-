from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def print_tasks(rows):
    if not rows:
        print('Nothing to do!')
    else:
        for i, task in enumerate(rows, start=1):
            print(f"{i}. {task.task}")


def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print('5) Add a task')
    print("6) Delete a task")
    print('0) Exit')


def main():
    session = Session()
    temp_file = open('temp.db', 'w', encoding='utf-8')

    while True:
        print()
        print_menu()
        user_choice = input()
        if user_choice == '1':
            today = datetime.today().date()
            rows = session.query(Task).filter(Task.deadline == today).all()
            print()
            print(f'Today {today.strftime("%d %b")}:')
            print_tasks(rows)
        elif user_choice == '2':
            today = datetime.today().date()
            for i in range(7):
                day = today + timedelta(days=i)
                rows = session.query(Task).filter(Task.deadline == day).all()
                print()
                print(f'{day.strftime("%A %d %b")}:')
                print_tasks(rows)
        elif user_choice == '3':
            rows = session.query(Task).order_by(Task.deadline).all()
            print()
            print("All tasks:")
            if not rows:
                print('Nothing to do!')
            else:
                for i, task in enumerate(rows, start=1):
                    print(f"{i}. {task.task}. {task.deadline.strftime('%#d %b')}")

        elif user_choice == '4':
            today = datetime.today().date()
            rows = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()
            print()
            print('Missed tasks:')
            if not rows:
                print('All tasks have been completed! ')
            else:
                for i, task in enumerate(rows, start=1):
                    print(f"{i}. {task.task}")
        elif user_choice == '5':
            task_description = input('Enter a task\n')
            task_deadline = datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d').date()
            new_task = Task(task=task_description, deadline=task_deadline)
            session.add(new_task)
            session.commit()
            print('The task has been added!\n')
        elif user_choice == '6':
            print("Choose the number of the task you want to delete:")
            rows = session.query(Task).order_by(Task.deadline).all()
            if not rows:
                print('Nothing to delete!')
            else:
                for i, task in enumerate(rows, start=1):
                    print(f"{i}. {task.task}. {task.deadline.strftime('%#d %b')}")
            deleted_task = int(input())
            specific_row = rows[deleted_task - 1]
            session.delete(specific_row)
            session.commit()
            print('The task has been deleted!')

        elif user_choice == '0':
            print('Bye!')
            print()
            break

    temp_file.close()  # Close the file after reading its contents


if __name__ == '__main__':
    main()
