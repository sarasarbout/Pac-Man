from parser.config_parser import ConfigParser, ConfigError


def main() -> None:
    try:
        parser = ConfigParser("config.json")
        config = parser.config_data

        print("\n--- CONFIG LOADED ---")
        print("Highscore file:", config.highscore_filename)
        print("Lives:", config.lives)
        print("Level max time:", config.level_max_time)
        print("Pacgum points:", config.points_per_pacgum)
        print("Super pacgum points:", config.points_per_super_pacgum)
        print("Ghost points:", config.points_per_ghost)

        print("\n--- LEVELS ---")
        for i, level in enumerate(config.levels, start=1):
            print(f"Level {i}: {level}")

    except ConfigError as error:
        print(f"Configuration error: {error}")


if __name__ == "__main__":
    main()
