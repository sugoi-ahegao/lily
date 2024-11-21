from tests.testing_utils.generic import generic

generated_ids: set[int] = set()


def generate_random_unique_id() -> int:
    new_id = generic.random.randint(1, 10_000)

    if new_id in generated_ids:
        return generate_random_unique_id()

    generated_ids.add(new_id)

    return new_id
