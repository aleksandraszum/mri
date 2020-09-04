from course.models import LessonContent, Lesson


def push_content(lesson_id, part_of_the_lesson):
    css = Lesson.objects.get(pk=lesson_id).css
    js = Lesson.objects.get(pk=lesson_id).js
    title = Lesson.objects.get(pk=lesson_id).title
    content = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=part_of_the_lesson).content

    return css, js, title, content


def last_next_content(lesson_id, part_of_the_lesson):
    previous = True
    sequent = True

    p_idx = int(part_of_the_lesson) - 1
    s_idx = int(part_of_the_lesson) + 1

    try:
        p = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=p_idx)
    except LessonContent.DoesNotExist:
        previous = False

    try:
        n = LessonContent.objects.get(lesson_id=lesson_id, part_of_the_lesson=s_idx)
    except LessonContent.DoesNotExist:
        sequent = False

    return previous, sequent, p_idx, s_idx
