
class Loader:
    @staticmethod
    def load(filename):
        content = ""
        with open(filename, 'r') as f:
            for line in f.readlines():
                content += line.strip()
        return content


class Dumper:
    @staticmethod
    def dump(content, filename):
        with open(filename, 'w') as f:
            f.write(content)
