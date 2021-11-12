from django.shortcuts import render

# Create your views here.

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']



class RegisterView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = RegisterSerializer
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        serializer.save()
        res = {}
        try:
            user = User.objects.get(
                email=serializer_data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=status.HTTP_200_OK)
        if user.is_active:
            res.update(
                {
                    'success_message': 'Account creation was successful',
                    'status': status.HTTP_201_CREATED,
                    'refresh': user.tokens()['refresh'],
                    'access': user.tokens()['access']
                }
            )
        else:
            res.update({
                'activate account': 'please check your email to activate account'
            })
        return Response(res, status=res.get('status'))
