from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from .models import Contributor, CustomProject, Issue
from .serializers import ContributorSerializer, CustomProjectSerializer, IssueSerializer
from rest_framework.permissions import IsAuthenticated


class CustomProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        data = request.data.copy()
        data["author"] = request.user
        serializer = CustomProjectSerializer(data=data)
        print('serializer', serializer)
        if serializer.is_valid():
            project = serializer.save(author=data["author"])

            Contributor.objects.create(user=request.user, project=project)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return CustomProject.objects.get(pk=pk)
        except CustomProject.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None):
        if pk:
            project = self.get_object(pk)
            serializer = CustomProjectSerializer(project)
            return Response(serializer.data)
        projects = CustomProject.objects.all()
        serializer = CustomProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = CustomProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(CustomProject, id=project_id)
        print("project", project)
        if project.author != request.user:
            return Response({"error": "Only the author of the project can add contributors."}, status=status.HTTP_403_FORBIDDEN)
        
        username_to_add = request.data.get("username")
        if not username_to_add:
            return Response({"error": "Username to add is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_to_add = CustomUser.objects.get(username=username_to_add)
            print("user_to_add", user_to_add)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if Contributor.objects.filter(user=user_to_add, project=project).exists():
            return Response({"error": "User is already a contributor to this project"}, status=status.HTTP_400_BAD_REQUEST)

        contributor = Contributor(user=user_to_add, project=project)
        print("contributor", contributor)
        contributor.save()

        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectContributorsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user_id=None):
        if user_id is not None:

            try:
                project = get_object_or_404(CustomProject, id=project_id)
                return Contributor.objects.get(project=project, user_id=user_id)
            except Contributor.DoesNotExist:
                raise Http404
        else:

            project = get_object_or_404(CustomProject, id=project_id)
            return Contributor.objects.filter(project=project)

    def get(self, request, project_id, user_id=None):
        if user_id is not None:

            contributor = self.get_object(project_id, user_id)
            serializer = ContributorSerializer(contributor)
            return Response(serializer.data)
        else:

            contributors = self.get_object(project_id)
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)

    def delete(self, request, project_id, user_id):
        project = get_object_or_404(CustomProject, id=project_id)
        
        if project.author != request.user:
            return Response({"error": "Only the author of the project can remove contributors."}, status=status.HTTP_403_FORBIDDEN)

        contributor = self.get_object(project_id, user_id)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IssueCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, project_id):
       
        project = get_object_or_404(CustomProject, id=project_id)
        if not Contributor.objects.filter(user=request.user, project=project).exists():
            return Response({"error": "You must be a contributor of the project to create an issue."},
                            status=status.HTTP_403_FORBIDDEN)
      
        serializer = IssueSerializer(data=request.data)
        
        if serializer.is_valid():
            print(request.data['user'])
            serializer.validated_data['created_by'] = Contributor.objects.get(user=request.user, project=project)
            serializer.validated_data['project'] = project
            
            user_work_on = get_object_or_404(CustomUser, username=request.data['user'])
            serializer.validated_data['user'] = Contributor.objects.get(user=user_work_on, project=project)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectIssueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, issue_id=None):
        project = get_object_or_404(CustomProject, id=project_id)
        if issue_id:
            return get_object_or_404(Issue, id=issue_id, project=project)
        else:
            return Issue.objects.filter(project=project)

    def get(self, request, project_id, issue_id=None):
        if issue_id:
            issue = self.get_object(project_id, issue_id)
            serializer = IssueSerializer(issue)
            return Response(serializer.data)
        else:
            issues = self.get_object(project_id)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data)


    def put(self, request, project_id, issue_id):
        project = get_object_or_404(CustomProject, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)

        if request.user == issue.user or request.user == project.author:
            serializer = IssueSerializer(issue, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only the issue creator or project author can modify this issue."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, project_id, issue_id):
        project = get_object_or_404(CustomProject, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)
        
        if issue.user != request.user and project.author != request.user:
            return Response({"error": "Only the issue creator or project author can delete this issue."}, status=status.HTTP_403_FORBIDDEN)
        
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectUserIssuesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, user_id):
        try:
            project = CustomProject.objects.get(id=project_id)
        except Contributor.DoesNotExist:
            return Response({"error": "You are not a contributor of this project."}, status=status.HTTP_403_FORBIDDEN)
        except CustomProject.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            specified_user = CustomUser.objects.get(id=user_id)
            Contributor.objects.get(project=project, user=specified_user)
        except Contributor.DoesNotExist:
            return Response({"error": "Specified user is not a contributor to this project."}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"error": "Specified user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        issues = Issue.objects.filter(user=specified_user, project=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)





