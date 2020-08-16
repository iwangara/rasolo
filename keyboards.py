#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import create_deep_linked_url

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def main_menu():
    button_list =[]
    for language in config.LANGUAGES:
        inline = InlineKeyboardButton(f"{language}",switch_inline_query_current_chat=f"{language}")
        button_list.append(inline)

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup

def sub_menu(bot_type,language,context):
    link =create_deep_linked_url(context.bot.get_me().username, "some-params",group=False)
    button_list =[
        InlineKeyboardButton(f"🎲 Select", switch_inline_query_current_chat =f"{bot_type}"),
        InlineKeyboardButton(f"🔙 Back", switch_inline_query_current_chat=f"{language}"),
        InlineKeyboardButton(f"🔁 Share", switch_inline_query=f"{language}"),
        InlineKeyboardButton(f"↩️ Restart", url=link,),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup

def answer_menu(language):

    button_list =[
        InlineKeyboardButton(f"🎲 Select",callback_data="yes"),
        InlineKeyboardButton(f"🔙 Back", switch_inline_query_current_chat=f"{language}"),

    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup

def play_menu(bot_type,language,level,context):
    link =create_deep_linked_url(context.bot.get_me().username, "some-params",group=False)
    button_list =[
        InlineKeyboardButton(f"▶️ Play",callback_data=f"play+{bot_type}+{level}"),
        InlineKeyboardButton(f"🔙 Back", switch_inline_query_current_chat=f"{language}"),
        InlineKeyboardButton(f"🔁 Share", switch_inline_query=f"{language}"),
        InlineKeyboardButton(f"↩️ Restart", url=link,),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup

def back_key(language):
    button_list = [
        InlineKeyboardButton(f"🔙 Back", switch_inline_query_current_chat=f"{language}"),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return reply_markup

def next_question(language,bot_type,level):
    button_list = [
        InlineKeyboardButton(f"🔙 Back", switch_inline_query_current_chat=f"{language}"),
        InlineKeyboardButton(f"⏭️ Next", callback_data=f"play+{bot_type}+{level}"),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup
