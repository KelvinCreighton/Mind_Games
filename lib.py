
def in_screen(screen, rect):
    screen_width, screen_height = screen.get_size()

    return 0 <= rect.left < screen_width and 0 <= rect.top < screen_height and \
           0 <= rect.right <= screen_width and 0 <= rect.bottom <= screen_height