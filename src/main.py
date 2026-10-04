from config_parser import ConfigParser, ParsingError

try:
    parser = ConfigParser()
    content = parser.read_file("config.json")
    text = parser.strip_comments(content)
    print(parser.parse_json(text))
except ParsingError as e:
    print(e)

