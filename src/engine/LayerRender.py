from pygame.sprite import LayeredUpdates as LU


class LayerRender(LU):

    def draw(self, system):
        """
        Sobrescreve a função draw original do pygame, para uso da função blit da
        System
        :param system: objeto System
        :return: list de Rects
        """
        rect_list = list()
        for sprite in self.sprites():
            if sprite.renderable:
                sprite.render()
                rect_list.append(sprite.dest)
        return rect_list