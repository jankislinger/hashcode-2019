from inout import combine_verticals, arrange_by_tags


def prepare_slides(photos):
    verticals = [photo for photo in photos if not photo.is_horizontal]
    verticals = merge_verticals(verticals)
    horizontals = [photo for photo in photos if photo.is_horizontal]
    return arrange_by_tags(verticals + horizontals)


def create_vertical_slides(verticals):
    n = 2 * (len(verticals) // 2)
    return [combine_verticals(verticals[i], verticals[i + 1]) for i in range(0, n, 2)]


def merge_verticals(vertical_photos, next_n=100):
    vertical_photos = set(vertical_photos)
    out = []

    while vertical_photos:
        v_photo = vertical_photos.pop()
        if not vertical_photos:
            break

        min_photo = None
        min_value = 1000
        i = 0

        # for n in range(order + 1, min(n_vertical_photos, order + next_n)):

        for other in vertical_photos:
            trans_value = len(v_photo.tags & other.tags)

            if trans_value < min_value:
                min_value = trans_value
                min_photo = other
                if min_value == 0:
                    break

            i += 1
            if i >= next_n:
                break

        vertical_photos.remove(min_photo)
        out.append(combine_verticals(v_photo, min_photo))

    return out
