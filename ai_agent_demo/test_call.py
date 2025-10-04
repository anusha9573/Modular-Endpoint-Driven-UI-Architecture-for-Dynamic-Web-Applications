from backend.agents.coordinator import Coordinator


def main():
    coord = Coordinator()
    tasks = coord.process_brief('Build a todo app with authentication and a REST API.')
    print('Generated tasks:')
    for t in tasks:
        print('-', t)


if __name__ == '__main__':
    main()
