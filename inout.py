from typing import Set, List

from dataclasses import dataclass


@dataclass
class Photo:
    index: str
    is_horizontal: bool
    num_tags: int
    tags: Set

    @classmethod
    def from_line(cls, index, line):
        line = line.rstrip().split(' ')
        num_tags = int(line[1])
        # tags = set(hash(tag) for tag in line[2:])
        tags = set(tag for tag in line[2:])
        assert len(tags) == num_tags
        return cls(index, line[0] == 'H', num_tags, tags)

    def __hash__(self):
        return hash(self.index)


Slideshow = List[Photo]


def transition_value(a: Photo, b: Photo):
    return min(
        len(a.tags - b.tags),
        len(b.tags - a.tags),
        len(a.tags & b.tags)
    )


def combine_verticals(a: Photo, b: Photo):
    assert not a.is_horizontal and not b.is_horizontal
    new_tags = a.tags | b.tags
    return Photo(f"{a.index} {b.index}", False, len(new_tags), new_tags)


def evaluate_slideshow(slideshow: Slideshow):
    return sum(transition_value(a, b) for a, b in zip(slideshow[:-1], slideshow[1:]))


def arrange_by_tags(slideshow, decreasing=True):
    return sorted(slideshow, reverse=decreasing, key=lambda x: x.num_tags)


def read(file_name):
    with open(file_name) as file:
        N = int(file.readline())
        return [Photo.from_line(str(i), file.readline()) for i in range(N)]


def write(slideshow, data_size):
    file_name = f"output/{data_size}.txt"
    with open(file_name, 'w') as file:
        file.write(str(len(slideshow)) + "\n")
        for photo in slideshow:
            file.write(photo.index + "\n")


if __name__ == '__main__':
    photos = read('data/a_example.txt')
    print(combine_verticals(photos[2], photos[1]))
    print(transition_value(photos[2], photos[1]))
