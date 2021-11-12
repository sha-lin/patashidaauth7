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

# class RegisterView(generics.GenericAPIView):

#     serializer_class = RegisterSerializer
#     renderer_classes = (UserRenderer,)

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = User.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token
#         current_site = get_current_site(request).domain
#         relativeLink = reverse('email-verify')
#         absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         email_body = 'Hi '+user.username + \
#             ' Use the link below to verify your email \n' + absurl
#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Verify your email'}

#         Util.send_email(data)
#         return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
