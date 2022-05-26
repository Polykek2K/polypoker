from accounts.models import CustomUser as userDB
from poker.models import Room as roomDB
from tables.models import Table as tableDB
from poker.models import Players as playersDB


def database():
    user = userDB.objects.create_user(username='skorol', password='StrongPassW0rd')
    table = tableDB.objects.create(name='table', buyIn=300, maxNoOfPlayers=3)
    room = roomDB.objects.create(table=table)
    player = playersDB.objects.create(user=user, room=room, moneyInTable=100)
    return (user, table, room, player)

