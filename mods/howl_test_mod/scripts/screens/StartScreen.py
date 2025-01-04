from scripts.screens.StartScreen import *
import scripts.screens.StartScreen

from scripts.game_structure.screen_settings import game_screen_size

def _modify_button(self, var_name: str, old_button, new_button) -> None:
    """
    Args:
        var_name (str): the dotname of the button to be modified (e.g. "continue_button" from self.continue_button)
        old_button: old button to be replaced (directly from self, e.g. self.continue_button)
        new_button: the object to replace the original button with
    """
    for sprite in MANAGER.get_sprite_group():
        if sprite == old_button:
            sprite.kill()
            break
    else:
        return
    setattr(self, var_name, new_button)

class StartScreen(scripts.screens.StartScreen.StartScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def screen_switches(self):
        super().screen_switches()
        for button in [
            ["continue_button", self.continue_button], ["switch_clan_button", self.switch_clan_button],
            ["new_clan_button", self.new_clan_button], ["settings_button", self.settings_button],
            ["quit", self.quit]
        ]:
            is_enabled = button[1].is_enabled
            _modify_button(self, button[0], button[1], UISurfaceImageButton(
                ui_scale(pygame.Rect((game_screen_size[0]-270, button[1].relative_rect.top), (200, 30))),
                button[1].text,
                image_dict=get_button_dict(ButtonStyles.MAINMENU, (200, 30)),
                object_id="@buttonstyles_mainmenu",
                manager=MANAGER,
                anchors=button[1].anchors,
                visible=button[1].visible,
                )
            )
            if not is_enabled:
                getattr(self, button[0]).disable()