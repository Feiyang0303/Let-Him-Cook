def blender(self, player: int, objects: List) -> None:
        """ accecpt an integer and a list of the items to use. Romove the materirals from the inventrory and add the product to users inventory
        Args:
            player: the number represents the player who uses the blender
            objects: a list of the items to put into the blender
            """
        if player == 1:
            user = self.player
        elif player == 2:
            user = self.player2

        # cookie
        if "sugar" in objects:
            if "butter" in object:
                if "flour" in object:
                    user.inventory.remove("sugar")
                    user.inventory.remove("butter")
                    user.inventory.remove("flour")
                    user.inventory.add("cookie")
                    
        # cake
        if "sugar" in objects:
            if "egg" in object:
                if "flour" in object:
                    user.inventory.remove("sugar")
                    user.inventory.remove("egg")
                    user.inventory.remove("flour")
                    user.inventory.add("cake")
                    
        # weiner
        if "salt" in objects:
            if "beef" in object:
                if "water" in object:
                    user.inventory.remove("salt")
                    user.inventory.remove("beef")
                    user.inventory.remove("water")
                    user.inventory.add("weiner")