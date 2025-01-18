import pygame
import pygame_gui
import sys
import importlib

from pygame_gui.elements import UIImage
import pygame_gui.elements.ui_button

from scripts.game_structure.screen_settings import MANAGER
from scripts.screens.Screens import Screens
from scripts.utility import (
    get_text_box_theme,
    ui_scale,
    ui_scale_dimensions,
    ui_scale_value,
    ui_scale_offset,
)
from scripts.game_structure.ui_elements import (
    UIImageButton
)
from scripts.utility import (
    quit,
)

from scripts.mod_loader.file_loader import FileHandler
from scripts.mod_loader.mod_loader import mods, toggle


class ModLoaderScreen(Screens):
    def screen_switches(self) -> None:
        super().screen_switches()
        self.set_bg("default", "mainmenu_bg")
        self.show_mute_buttons()

        self.toggled = False

        self.screen = pygame.transform.scale(
            pygame.image.load(FileHandler.get_path("resources/images/mods_list_frame.png")).convert_alpha(),
            ui_scale_dimensions((519, 383)),
        )
        self.mods_list_frame = UIImage(
            pygame.Rect(
                ui_scale_offset((0, 151)), (ui_scale_value(519), self.screen.height)
            ),
            self.screen,
            anchors={"centerx": "centerx"},
            starting_height=0,
        )
        self.info = pygame_gui.elements.UITextBox(
            "Note: Leaving this screen after toggling a mod will close the game.\nWhen you open it next, the mods will be updated.",
            # pylint: disable=line-too-long
            ui_scale(pygame.Rect((100, 550), (600, 70))),
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER,
        )

        self.mods_list = []
        self.versions = []
        self.tooltips = []
        self.checkboxes = []
        self.checkboxes_text = {}

        self.checkboxes_text[
            "container_general"
        ] = pygame_gui.elements.UIScrollingContainer(
            ui_scale(pygame.Rect((150, 190), (499, 334))),
            allow_scroll_x=False,
            manager=MANAGER,
        )

        mods_sorted = {k: v for k, v in sorted(mods.items(), key=lambda item: item[1].priority, reverse=True)}
        for mod in mods_sorted.values():
            self.mods_list.append(
                pygame_gui.elements.UITextBox(
                    mod.name,
                    ui_scale(pygame.Rect((32, 2 if len(self.mods_list) == 0 else 6), (343, 36))),
                    container=self.checkboxes_text["container_general"],
                    object_id=get_text_box_theme("#text_box_30_horizleft"),
                    manager=MANAGER,
                    anchors = {
                        "top_target": self.mods_list[-1]
                    } if len(self.mods_list) > 0 else None,
                    # tool_tip_text=f"{mod.name} by {mod.author}\n{mod.description}",
                )
            )
            self.tooltips.append(
                UIImageButton(
                    ui_scale(pygame.Rect((32, 2 if len(self.tooltips) == 0 else 6), (343, 36))),
                    "",
                    container=self.checkboxes_text["container_general"],
                    # object_id="#blank_button_dark"
                    # if game.settings["dark mode"]
                    # else "#blank_button",
                    manager=MANAGER,
                    starting_height=2,
                    anchors = {
                        "top_target": self.tooltips[-1]
                    } if len(self.tooltips) > 0 else None,
                    tool_tip_text=f"{mod.name} by {mod.author}\n{mod.description}",
                )
            )
            if mod.toggleable:
                self.checkboxes.append(
                    UIImageButton(
                        ui_scale(pygame.Rect((3, -35 ), (34, 34))),
                        "",
                        object_id="@checked_checkbox" if mod.enabled else "@unchecked_checkbox",
                        container=self.checkboxes_text["container_general"],
                        # tool_tip_text=f"mod_loader.{code}_tooltip",
                        anchors = {
                            "top_target": self.mods_list[-1],
                        }
                    )
                )
            else:
                self.checkboxes.append(None)

        self.menu_buttons["main_menu"].show()
    
    def handle_event(self, event) -> None:
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.menu_buttons["main_menu"]:
                self.change_screen("start screen")
            elif event.ui_element in self.checkboxes:
                mod = mods[self.mods_list[self.checkboxes.index(event.ui_element)].html_text]
                toggle(mod.name)
                self.toggled = True
                self.checkboxes[self.checkboxes.index(event.ui_element)].change_object_id(
                    "@checked_checkbox" if mod.enabled else "@unchecked_checkbox"
                )
                
    def exit_screen(self) -> None:
        super().exit_screen()
        self.mods_list_frame.kill()
        self.info.kill()
        self.checkboxes_text["container_general"].kill()
        [checkbox.kill() for checkbox in list(filter(None, self.checkboxes))]
        [mod.kill() for mod in self.mods_list]
        [tooltip.kill() for tooltip in self.tooltips]

        for module in sys.modules.copy():
            del sys.modules[module]
        
        if self.toggled:
            quit()