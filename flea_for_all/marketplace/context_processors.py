from .models import Conversation

def open_conversations(request):
    if not request.user.is_authenticated:
        return {"open_conversations": []}

    ids = request.session.get("open_conversation_ids", [])
    conversations = list(
        Conversation.objects.filter(pk__in=ids, participants=request.user).distinct()
    )
    for c in conversations:
        c.other_user = c.participants.exclude(pk=request.user.pk).first()
    return {"open_conversations": conversations}