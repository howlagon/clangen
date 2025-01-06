from scripts.screens.StartScreen import *

from scripts.game_structure.screen_settings import game_screen_size

class StartScreen(StartScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def screen_switches(self):
        super().screen_switches()
        for button in [
            ["continue_button", self.continue_button], ["switch_clan_button", self.switch_clan_button],
            ["new_clan_button", self.new_clan_button], ["settings_button", self.settings_button],
            ["quit", self.quit]
        ]:
            button_name, button = button
            is_enabled = button.is_enabled
            button.kill()
            new_button = UISurfaceImageButton(
                ui_scale(pygame.Rect((game_screen_size[0]-270, button.relative_rect.top), (200, 30))),
                button.text,
                image_dict=get_button_dict(ButtonStyles.MAINMENU, (200, 30)),
                object_id="@buttonstyles_mainmenu",
                manager=MANAGER,
                anchors=button.anchors,
                visible=button.visible,
            )
            setattr(self, button_name, new_button)
            if not is_enabled:
                new_button.disable()