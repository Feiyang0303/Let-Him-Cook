import unittest
import pygame as pg

from items import Item, Package, Inventory
from world import Counter, Processor


class FakeGame:
    def __init__(self):
        self.counter_recipes = {}
        self.oven_recipes = {}
        self.chopper_recipes = {}

        # Minimal sprites to avoid file I/O
        surf = pg.Surface((16, 16), pg.SRCALPHA)

        self.item_library = {
            "package": Package(self, "package", surf),
            "sugar": Item(self, "sugar", surf),
            "flour": Item(self, "flour", surf),
            "butter": Item(self, "butter", surf),
        }


class SimplePlayer:
    def __init__(self, game):
        self.inventory = Inventory(game, self)


class PickupDropTests(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = FakeGame()
        # Use simple Surfaces as building sprites
        sprite = pg.Surface((16, 16), pg.SRCALPHA)
        self.counter = Counter(self.game, "counter", sprite)
        self.processor = Processor(self.game, "chopper", sprite)
        self.player = SimplePlayer(self.game)

    def tearDown(self):
        pg.quit()

    # Counter: drop on empty counter
    def test_drop_item_on_empty_counter(self):
        self.player.inventory.add_item("sugar")
        self.counter.interact(self.player)
        self.assertIsNotNone(self.counter.item)
        self.assertEqual(self.counter.item.id, "sugar")
        self.assertTrue(self.player.inventory.isEmpty())

    # Counter: drop when counter already has item and player has item -> becomes a package
    def test_drop_item_on_counter_with_existing_item_results_in_package(self):
        self.counter.item = self.game.item_library["sugar"]
        self.player.inventory.add_item("flour")
        self.counter.interact(self.player)
        self.assertIsInstance(self.counter.item, Package)
        self.assertTrue(self.player.inventory.isEmpty())

    # Counter: pickup from counter adds to inventory and clears counter
    def test_pickup_from_counter(self):
        self.counter.item = self.game.item_library["flour"]
        self.counter.alt_interact(self.player)
        self.assertTrue(self.counter.item is None)
        self.assertFalse(self.player.inventory.isEmpty())
        self.assertEqual(self.player.inventory.next().id, "flour")

    # Counter: pickup should not occur if inventory is full
    def test_pickup_from_counter_inventory_full(self):
        for _ in range(Inventory.MAX):
            self.player.inventory.add_item("sugar")
        self.counter.item = self.game.item_library["flour"]
        self.counter.alt_interact(self.player)
        self.assertIsNotNone(self.counter.item)
        self.assertEqual(self.counter.item.id, "flour")

    # Counter: interacting with empty inventory should leave counter unchanged
    def test_drop_with_empty_inventory_does_nothing(self):
        self.assertTrue(self.player.inventory.isEmpty())
        self.assertIsNone(self.counter.item)
        self.counter.interact(self.player)
        self.assertIsNone(self.counter.item)

    # Processor: drop item becomes a package and resets progress
    def test_processor_drop_item_creates_package(self):
        self.player.inventory.add_item("sugar")
        self.processor.progress = 0.5
        self.processor.interact(self.player)
        self.assertIsInstance(self.processor.item, Package)
        self.assertEqual(self.processor.progress, 0)
        self.assertTrue(self.player.inventory.isEmpty())

    # Processor: pickup only allowed when progress complete
    def test_processor_pickup_requires_complete_progress(self):
        self.processor.item = self.game.item_library["sugar"]
        self.processor.progress = 0.9
        self.processor.alt_interact(self.player)
        self.assertIsNotNone(self.processor.item)
        self.assertTrue(self.player.inventory.isEmpty())

        self.processor.progress = 1.0
        self.processor.alt_interact(self.player)
        self.assertIsNone(self.processor.item)
        self.assertFalse(self.player.inventory.isEmpty())
        self.assertEqual(self.player.inventory.next().id, "sugar")


if __name__ == "__main__":
    unittest.main()


