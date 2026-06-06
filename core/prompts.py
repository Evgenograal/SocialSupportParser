from core.settings import get_settings


def build_prompt(text: str):
    template = get_settings("prompt_template")

    return template.format(
        categories="\n".join(
            get_settings("categories", [])
        ),

        life_situations="\n".join(
            get_settings("life_situations", [])
        ),

        family_statuses="\n".join(
            get_settings("family_statuses", [])
        ),

        territories="\n".join(
            get_settings("territories", [])
        ),

        text=text
    )