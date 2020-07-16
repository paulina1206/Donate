def get_header_class(request):
    if request.path == '/':
        return {'header_class': "header--main-page"}
    if request.path == '/adddonation/':
        return {'header_class': "header--form-page"}
    return {'header_class': ""}