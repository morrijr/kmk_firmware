import unittest

from kmk.keys import (
    KC,
    Key,
    ModifierKey,
    make_key,
    maybe_make_alpha_key,
    maybe_make_consumer_key,
    maybe_make_key,
    maybe_make_mod_key,
    maybe_make_numeric_key,
    maybe_make_shifted_key,
)
from tests.keyboard_test import KeyboardTest


class TestKmkKeys(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [],
            [
                [
                    KC.HASH,
                    KC.RALT(KC.HASH),
                    KC.RALT(KC.LSFT(KC.N3)),
                    KC.RALT(KC.LSFT),
                    # Note: this is correct, if unusual, syntax. It's a useful test because it failed silently on previous builds.
                    KC.RALT(KC.LSFT)(KC.N3),
                    KC.RALT,
                ]
            ],
        )
        keyboard.test(
            'Shifted key',
            [(0, True), (0, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                },
                {},
            ],
        )
        keyboard.test(
            'AltGr+Shifted key',
            [(1, True), (1, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'AltGr+Shift+key',
            [(2, True), (2, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'Shift+AltGr',
            [(3, True), (3, False)],
            [
                {
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'AltGr+Shift+key, alternate chaining',
            [(4, True), (4, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'AltGr',
            [(5, True), (5, False)],
            [
                {
                    KC.RALT,
                },
                {},
            ],
        )

        assert isinstance(KC.RGUI(no_press=True), ModifierKey)
        assert isinstance(KC.RALT(KC.RGUI), ModifierKey)
        assert isinstance(KC.Q(no_press=True), Key)
        assert not isinstance(KC.Q(no_press=True), ModifierKey)
        assert isinstance(KC.RALT(KC.Q), Key)
        assert not isinstance(KC.RALT(KC.Q), ModifierKey)


class TestKeys_dot(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_expected_code_uppercase(self):
        assert 4 == KC.A.code

    def test_expected_code_lowercase(self):
        assert 4 == KC.a.code

    def test_case_ignored_alpha(self):
        upper_key = KC.A
        lower_key = KC.a
        assert upper_key is lower_key

    def test_case_requested_order_irrelevant(self):
        lower_key = KC.a
        upper_key = KC.A
        assert upper_key is lower_key

    def test_secondary_name(self):
        primary_key = KC.NO
        secondary_key = KC.XXXXXXX
        assert primary_key is secondary_key

    def test_invalid_key_upper(self):
        with self.assertRaises(ValueError):
            KC.INVALID_KEY

    def test_invalid_key_lower(self):
        with self.assertRaises(ValueError):
            KC.invalid_key

    def test_custom_key(self):
        created = make_key(
            KC.N2.code,
            names=(
                'EURO',
                '€',
            ),
            has_modifiers={KC.LSFT.code, KC.ROPT.code},
        )
        assert created is KC.get('EURO')
        assert created is KC.get('€')

    def test_match_exactly_case(self):
        created = make_key(names=('ThIs_Is_A_StRaNgE_kEy',))
        assert created is KC.get('ThIs_Is_A_StRaNgE_kEy')


class TestKeys_index(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_expected_code_uppercase(self):
        assert 4 == KC['A'].code

    def test_expected_code_lowercase(self):
        assert 4 == KC['a'].code

    def test_case_ignored_alpha(self):
        upper_key = KC['A']
        lower_key = KC['a']
        assert upper_key is lower_key

    def test_case_requested_order_irrelevant(self):
        lower_key = KC['a']
        upper_key = KC['A']
        assert upper_key is lower_key

    def test_invalid_key_upper(self):
        with self.assertRaises(ValueError):
            KC['NOT_A_VALID_KEY']

    def test_invalid_key_lower(self):
        with self.assertRaises(ValueError):
            KC['not_a_valid_key']

    def test_custom_key(self):
        created = make_key(
            KC['N2'].code,
            names=(
                'EURO',
                '€',
            ),
            has_modifiers={KC['LSFT'].code, KC['ROPT'].code},
        )
        assert created is KC['EURO']
        assert created is KC['€']

    def test_match_exactly_case(self):
        created = make_key(names=('ThIs_Is_A_StRaNgE_kEy',))
        assert created is KC['ThIs_Is_A_StRaNgE_kEy']


class TestKeys_get(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_expected_code_uppercase(self):
        assert 4 == KC.get('A').code

    def test_expected_code_lowercase(self):
        assert 4 == KC.get('a').code

    def test_case_ignored_alpha(self):
        upper_key = KC.get('A')
        lower_key = KC.get('a')
        assert upper_key is lower_key

    def test_case_requested_order_irrelevant(self):
        lower_key = KC.get('a')
        upper_key = KC.get('A')
        assert upper_key is lower_key

    def test_secondary_name(self):
        primary_key = KC.NO
        secondary_key = KC.XXXXXXX
        assert primary_key is secondary_key

    def test_invalid_key_upper(self):
        assert KC.get('INVALID_KEY') is None

    def test_invalid_key_lower(self):
        assert KC.get('not_a_valid_key') is None

    def test_custom_key(self):
        created = make_key(
            KC.get('N2').code,
            names=(
                'EURO',
                '€',
            ),
            has_modifiers={KC.get('LSFT').code, KC.get('ROPT').code},
        )
        assert created is KC.get('EURO')
        assert created is KC.get('€')

    def test_match_exactly_case(self):
        created = make_key(names=('ThIs_Is_A_StRaNgE_kEy',))
        assert created is KC.get('ThIs_Is_A_StRaNgE_kEy')


# Some of these test appear silly, but they're testing we get the
# same, single, instance back when requested through KC and that
# order of request doesn't matter
class TestKeys_instances(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_make_key_new_instance(self):
        key1 = make_key(code=1)
        key2 = make_key(code=1)
        assert key1 is not key2
        assert key1.code == key2.code

    def test_index_is_index(self):
        assert KC['A'] is KC['A']

    def test_index_is_dot(self):
        assert KC['A'] is KC.A

    def test_index_is_get(self):
        assert KC['A'] is KC.get('A')

    def test_dot_is_dot(self):
        assert KC.A is KC.A

    def test_dot_is_index(self):
        assert KC.A is KC['A']

    def test_dot_is_get(self):
        assert KC.A is KC.get('A')

    def test_get_is_get(self):
        assert KC.get('A') is KC.get('A')

    def test_get_is_index(self):
        assert KC.get('A') is KC['A']

    def test_get_is_dot(self):
        assert KC.get('A') is KC.A


class TestKeys_make_key(unittest.TestCase):
    # TODO: make_key functionality general tests

    def test_maybe_no_candidate(self):
        assert maybe_make_key('a', None, ('b', 'c')) is None

    def test_maybe_with_code(self):
        key = maybe_make_key('c', 2, ('b', 'c'))
        assert key is not None
        assert key.code == 2
        assert key.has_modifiers is None


class TestKeys_make_mod_key(unittest.TestCase):
    # TODO: make_mod_key functionality general tests

    def test_maybe_no_candidate(self):
        assert maybe_make_mod_key('a', 3, ('b', 'c')) is None

    def test_maybe_candidate(self):
        key = maybe_make_mod_key('c', 3, ('b', 'c'))
        assert key is not None
        assert key.code == 3
        assert key.has_modifiers is None
        # TODO: What to check for a mod key?


class TestKeys_make_shifted_key(unittest.TestCase):
    # TODO: make_shifted_key functionality general tests

    def test_maybe_no_candidate(self):
        assert maybe_make_shifted_key('a', 4, ('b', 'c')) is None

    def test_maybe_candidate(self):
        key = maybe_make_shifted_key('c', 4, ('b', 'c'))
        assert key is not None
        assert key.code == 4
        assert key.has_modifiers == {2}


class TestKeys_make_consumer_key(unittest.TestCase):
    # TODO: make_consumer_key general tests

    def test_maybe_no_candidate(self):
        assert maybe_make_consumer_key('a', 3, ('b', 'c')) is None

    def test_maybe_candidate(self):
        key = maybe_make_consumer_key('c', 3, ('b', 'c'))
        assert key is not None
        assert key.code == 3
        assert key.has_modifiers is None
        # TODO: What to assert for a consumer key?


class TestKeys_maybe_make_alpha_key(unittest.TestCase):
    def test_not_alpha(self):
        assert maybe_make_alpha_key('1') is None

    def test_too_long(self):
        assert maybe_make_alpha_key('NO') is None

    def test_lower(self):
        key = maybe_make_alpha_key('c')
        assert key is not None
        assert key.code == 6
        assert key.has_modifiers is None

    def test_upper(self):
        key = maybe_make_alpha_key('C')
        assert key is not None
        assert key.code == 6
        assert key.has_modifiers is None


class TestKeys_maybe_make_numeric_key(unittest.TestCase):
    def test_no_candidate(self):
        assert maybe_make_numeric_key('a') is None

    def test_zero(self):
        key = maybe_make_numeric_key('0')
        assert key is not None
        assert key.code == 39
        assert key.has_modifiers is None

    def test_one(self):
        key = maybe_make_numeric_key('1')
        assert key is not None
        assert key.code == 30
        assert key.has_modifiers is None

    def test_nine(self):
        key = maybe_make_numeric_key('9')
        assert key is not None
        assert key.code == 38
        assert key.has_modifiers is None


if __name__ == '__main__':
    unittest.main()
