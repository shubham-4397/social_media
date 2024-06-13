"""
messages file
"""

SUCCESS_MESSAGE = {
    'request-sent': 'Request sent successfully',
    'request-accepted': 'Request has been accepted successfully',
    'request-rejected': 'Request has been rejected successfully'

}

ERROR_MESSAGE = {
    'request-not-found': 'Request with this id does not exist',
    'user-not-found': 'User with this id does not exist',
    'self-request': 'You cannot send a friend request to yourself',
    'request-already-exist': 'This request already exist',
    'request-exceed': 'up to 3 requests allowed in a minute'
}
