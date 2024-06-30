import streamlit as st
import markdown
from resume_analyzer import get_section_scores


def custom_markdown(
    text,
    html_tag="p",
    bg_color="white",
    color="black",
    font_size=None,
    text_align="left",
):
    """Customise markdown by specifying custom background colour, text colour, font size, and text alignment.."""

    style = f'style="background-color:{bg_color};color:{color};font-size:{font_size}px; \
text-align: {text_align};padding: 25px 25px 25px 25px;border-radius:2%;"'

    body = f"<{html_tag} {style}> {text}</{html_tag}>"

    st.markdown(body, unsafe_allow_html=True)
    st.write("")


def set_background_color(score):
    """Set background color based on score."""
    if score >= 80:
        bg_color = "#D4F1F4"
    elif score >= 60:
        bg_color = "#ededed"
    else:
        bg_color = "#fbcccd"
    return bg_color


def format_object_to_string(object, separator="\n- "):
    """Convert object (e.g. list) to string."""
    if not isinstance(object, str):
        return separator + separator.join(object)
    else:
        return object


def markdown_to_html(md_text):
    """Convert Markdown to html."""
    html_txt = (
        markdown.markdown(md_text.replace("\\n", "\n").replace("- ", "\n- "))
        .replace("\n", "")
        .replace('\\"', '"')
    )
    return html_txt


def display_scores_in_columns(section_names: list, scores: list, column_width: list):
    """Display the scores of the sections in side-by-side columns.
    The column_width variable sets the width of the columns."""
    columns = st.columns(column_width)
    for i, column in enumerate(columns):
        with column:
            custom_markdown(
                text=f"<b>{section_names[i]} <br><br> {scores[i]}</b>",
                bg_color=set_background_color(scores[i]),
                text_align="center",
            )


def display_section_results(
    expander_label: str,
    expander_header_fields: list,
    expander_header_links: list,
    score: int,
    section_original_text_header: str,
    section_original_text: list,
    original_text_bullet_points: bool,
    section_assessment,
    section_improved_text,
):
    if score > -1:
        expander_label += f"- 🎯 **{score}**/100"
    with st.expander(expander_label):
        st.write("")

        # 1. Display the header fields (for example, the company and dates of the work experience)
        if expander_header_fields is not None:
            for field in expander_header_fields:
                if not isinstance(field, list):
                    st.markdown(field)
                else:
                    # display fields in side-by-side columns.
                    columns = st.columns(len(field))
                    for i, column in enumerate(columns):
                        with column:
                            st.markdown(field[i])

        # 2. View the links (examle social media blogs and web sites)
        if expander_header_links is not None:
            if not isinstance(expander_header_links, list):
                link = expander_header_links.strip().replace('"', "")
                if not link.startswith("http"):
                    link = "https://" + link
                st.markdown(
                    f"""🌐 <a href="{link}" target="_blank">{link}""",
                    unsafe_allow_html=True,
                )
            else:
                for link in expander_header_links:
                    if not link.startswith("http"):
                        link = "https://" + link
                    st.markdown(
                        f"""🌐 <a href="{link}" target="_blank">{link}""",
                        unsafe_allow_html=True,
                    )

        # 3. View the original text
        if section_original_text_header is not None:
            st.write("")
            st.markdown(section_original_text_header)
        if section_original_text is not None:
            for text in section_original_text:
                if original_text_bullet_points:
                    st.markdown(f"- {text}")
                else:
                    st.markdown(text)

        # 4. Display of section score
        st.divider()
        custom_markdown(
            html_tag="h4",
            text=f"<b>🎯 Score: {score}</b>/<small>100</small>",
        )

        # 5. Display the assessmnet
        bg_color = set_background_color(score)
        assessment = markdown_to_html(format_object_to_string(section_assessment))
        custom_markdown(
            text=f"<b>🔎 Assessment:</b> <br><br> {assessment}",
            html_tag="div",
            bg_color=bg_color,
        )

        # 6. View the improved text
        if section_improved_text is not None:
            improved_text = markdown_to_html(
                format_object_to_string(section_improved_text)
            )
            custom_markdown(
                text=f"<b>🚀 Improvement:</b> <br><br> {improved_text}",
                html_tag="div",
                bg_color="#ededed",
            )
        st.write("")


def display_assessment(score, section_assessment):
    """Display the section score and the assessment."""
    # 1. View section score
    custom_markdown(
        html_tag="h4",
        text=f"<b>🎯 Score: {score}</b>/<small>100</small>",
    )
    # 2. Display the assessmnet
    bg_color = set_background_color(score)
    assessment = markdown_to_html(format_object_to_string(section_assessment))
    custom_markdown(
        text=f"<b>🔎 Assessment:</b> <br><br> {assessment}",
        html_tag="div",
        bg_color=bg_color,
    )
    st.write("")

def display_resume_analysism(SCANNED_RESUME):
    """Display the resume analysis."""
    try:
        st.title("Resume keypoints as per the Job description")
        st.subheader("Job Description Match")
        st.write(SCANNED_RESUME['JD_Match'])
        
        st.subheader("Missing Keywords")
        st.write(", ".join(SCANNED_RESUME['MissingKeywords']))
        
        st.write(SCANNED_RESUME['Profile_Summary'])

        st.subheader("Suggestions")
        for suggestion in SCANNED_RESUME['tailor_Suggetions']:
            st.write(f"- {suggestion}")
       
       
    except Exception as exception:
        print(exception)