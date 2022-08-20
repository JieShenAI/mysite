try:
    response = FileResponse(open(fileLocation, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + \
            os.path.basename(filename)
        return response
    except Exception:
        raise Http404
