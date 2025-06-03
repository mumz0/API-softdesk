from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.permissions import CommentPermissions, ProjectPermissions
from users.models import CustomUser
from .models import Contributor, CustomProject, Issue, Comment
from .serializers import CommentSerializer, ContributorSerializer, CustomProjectSerializer, IssueSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class ProjectAPIView(APIView):
    """
    API view for managing CustomProject instances.
    This view provides CRUD operations for projects with authentication and permission checks.
    Users can create, retrieve, update, and delete projects. When a project is created,
    the author is automatically added as a contributor.
    Permissions:
        - IsAuthenticated: User must be logged in
        - ProjectPermissions: Custom project-level permissions
    """
    permission_classes = [IsAuthenticated, ProjectPermissions]
    
    
    def get_object(self, pk):
        """
        Retrieve a CustomProject instance by primary key.

        Args:
            pk: The primary key of the CustomProject to retrieve.
        Returns:
            CustomProject: The CustomProject instance with the specified primary key.
        Raises:
            Http404: If no CustomProject with the given primary key exists.
        """
        try:
            return CustomProject.objects.get(pk=pk)
        except CustomProject.DoesNotExist:
            raise Http404
    
    
    def get(self, request, pk=None):
        """
        Retrieve a single project or list all projects.

        Args:
            request: The HTTP request object.
            pk (int, optional): Primary key of the project to retrieve. 
                               If None, returns all projects.
        Returns:
            Response: JSON response containing either:
                - Single project data when pk is provided
                - List of all projects when pk is None
        Raises:
            Http404: When project with given pk does not exist.
        """
        if pk:
            project = self.get_object(pk)
            serializer = CustomProjectSerializer(project)
            return Response(serializer.data)
        projects = CustomProject.objects.all()
        serializer = CustomProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        """
        Create a new project with the authenticated user as the author.
        
        This method handles POST requests to create a new project. The authenticated
        user is automatically set as the project author and added as a contributor.
        
        Args:
            request: HTTP request object containing project data and authenticated user  
        Returns:
            Response: JSON response with created project data and 201 status on success,
                     or validation errors with 400 status on failure     
        """
        data = request.data.copy()
        data["author"] = request.user
        serializer = CustomProjectSerializer(data=data)
        print('serializer', serializer)
        if serializer.is_valid():
            project = serializer.save(author=data["author"])
            Contributor.objects.create(user=request.user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, pk):
        """
        Update an existing project with provided data.

        Args:
            request: HTTP request object containing the updated project data
            pk: Primary key of the project to be updated
        Returns:
            Response: JSON response containing the updated project data if successful,
                     or validation errors with 400 status code if data is invalid
        Raises:
            Http404: If project with given pk does not exist
        """
        project = self.get_object(pk)
        serializer = CustomProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        """
        Delete a project instance.

        Args:
            request: The HTTP request object.
            pk: Primary key of the project to be deleted.
        Returns:
            Response: HTTP 204 No Content status upon successful deletion.
        Raises:
            Http404: If the project with the given pk does not exist.
        """
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectContributorsView(APIView):
    """
    API view for managing project contributors.
    This view handles CRUD operations for contributors within a project:
    - GET: Retrieve a specific contributor or list all contributors for a project
    - POST: Add a new contributor to a project by username
    - DELETE: Remove a contributor from a project (author only)
    The view supports both individual contributor operations (when user_id is provided)
    and bulk operations on all contributors for a project.
    Permissions:
        - IsAuthenticated: Only authenticated users can access this view
        - Project author: Only project authors can delete contributors
    URL Patterns:
        - GET /projects/{project_id}/contributors/ - List all contributors
        - GET /projects/{project_id}/contributors/{user_id}/ - Get specific contributor
        - POST /projects/{project_id}/contributors/ - Add new contributor
        - DELETE /projects/{project_id}/contributors/{user_id}/ - Remove contributor
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user_id=None):
        """
        Retrieve contributor(s) for a given project.
        Args:
            project_id (int): The ID of the project to look up contributors for.
            user_id (int, optional): The ID of a specific user. If provided, returns
                the specific contributor object for that user in the project.
                If None, returns all contributors for the project.
        Returns:
            Contributor: If user_id is provided, returns a single Contributor object
                for the specified user in the project.
            QuerySet: If user_id is None, returns a QuerySet of all Contributor
                objects for the project.
        Raises:
            Http404: If the project with the given project_id does not exist, or
                if a user_id is provided but no contributor relationship exists
                between that user and the project.
        """
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
        """
        Retrieve contributor(s) for a specific project.
        Args:
            request: The HTTP request object
            project_id: The ID of the project to get contributors for
            user_id (optional): The ID of a specific contributor. If provided,
                               returns only that contributor; otherwise returns all contributors
        Returns:
            Response: JSON response containing either:
                - A single contributor's data if user_id is provided
                - A list of all contributors for the project if user_id is None
        """
        if user_id is not None:

            contributor = self.get_object(project_id, user_id)
            serializer = ContributorSerializer(contributor)
            return Response(serializer.data)
        else:

            contributors = self.get_object(project_id)
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)

    
    def post(self, request, project_id):
        """
        Add a contributor to a project.
        This endpoint allows adding a user as a contributor to a specific project
        by providing their username in the request data.
        Args:
            request: HTTP request object containing the username to add
            project_id (int): ID of the project to add the contributor to
        Request Data:
            username (str): Username of the user to add as contributor
        Returns:
            Response: JSON response with one of the following:
                - 201: Successfully created contributor with serialized data
                - 400: Bad request if username missing or user already contributor
                - 404: Not found if project or user doesn't exist
        Raises:
            Http404: If project with given ID doesn't exist
        """
        project = get_object_or_404(CustomProject, id=project_id)
        username_to_add = request.data.get("username")
        if not username_to_add:
            return Response({"error": "Username to add is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_to_add = CustomUser.objects.get(username=username_to_add)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if Contributor.objects.filter(user=user_to_add, project=project).exists():
            return Response({"error": "User is already a contributor to this project"}, status=status.HTTP_400_BAD_REQUEST)

        contributor = Contributor(user=user_to_add, project=project)
        contributor.save()

        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def delete(self, request, project_id, user_id):
        """
        Remove a contributor from a project.
        This method allows the project author to remove a contributor from their project.
        Only the author of the project has permission to remove contributors.
        Args:
            request: The HTTP request object containing user authentication data.
            project_id (int): The unique identifier of the project.
            user_id (int): The unique identifier of the user to be removed as contributor.
        Returns:
            Response: HTTP 204 No Content on successful deletion.
            Response: HTTP 403 Forbidden if the requesting user is not the project author.
            Response: HTTP 404 Not Found if the project or contributor doesn't exist.
        Raises:
            Http404: If the project with the given project_id doesn't exist.
        """
        project = get_object_or_404(CustomProject, id=project_id)
        
        if project.author != request.user:
            return Response({"error": "Only the author of the project can remove contributors."}, status=status.HTTP_403_FORBIDDEN)

        contributor = self.get_object(project_id, user_id)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectIssueAPIView(APIView):
    """
    API view for managing issues within projects.
    This view handles CRUD operations for issues that belong to specific projects.
    All operations require authentication and proper project permissions.
    Endpoints:
        GET /projects/{project_id}/issues/ - List all issues for a project
        GET /projects/{project_id}/issues/{issue_id}/ - Retrieve a specific issue
        POST /projects/{project_id}/issues/ - Create a new issue (contributors only)
        PUT /projects/{project_id}/issues/{issue_id}/ - Update an issue (creator or project author only)
        DELETE /projects/{project_id}/issues/{issue_id}/ - Delete an issue (creator or project author only)
    Permissions:
        - User must be authenticated
        - User must have project permissions
        - POST: User must be a contributor of the project
        - PUT/DELETE: User must be the issue creator or project author
    """
    permission_classes = [IsAuthenticated, ProjectPermissions]


    def get_object(self, project_id, issue_id=None):
        """
        Retrieve a project or issue object based on provided IDs.

        Args:
            project_id (int): The ID of the project to retrieve.
            issue_id (int, optional): The ID of the specific issue to retrieve. 
                                     If None, returns all issues for the project.
        Returns:
            CustomProject or Issue or QuerySet: 
                - If issue_id is provided: Returns the specific Issue object
                - If issue_id is None: Returns a QuerySet of all Issue objects for the project
        Raises:
            Http404: If the project with the given project_id doesn't exist, or if 
                    the issue with the given issue_id doesn't exist in the specified project.
        """
        project = get_object_or_404(CustomProject, id=project_id)
        if issue_id:
            return get_object_or_404(Issue, id=issue_id, project=project)
        else:
            return Issue.objects.filter(project=project)


    def get(self, request, project_id, issue_id=None):
        """
        Retrieve issue(s) for a specific project.
        
        Args:
            request: The HTTP request object
            project_id: ID of the project to retrieve issues from
            issue_id (optional): ID of a specific issue to retrieve
        Returns:
            Response: JSON response containing either:
                - Single issue data if issue_id is provided
                - List of all issues for the project if issue_id is None
        Raises:
            Http404: If the project or issue does not exist
        """
        if issue_id:
            issue = self.get_object(project_id, issue_id)
            serializer = IssueSerializer(issue)
            return Response(serializer.data)
        else:
            issues = self.get_object(project_id)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data)

    def post(self, request, project_id):
        """
        Create a new issue for a specific project.
        This endpoint allows contributors of a project to create new issues.
        The user must be a contributor to the project to create an issue.
        Args:
            request: HTTP request object containing issue data
            project_id: ID of the project where the issue will be created
        Returns:
            Response: 
                - 201 CREATED with serialized issue data if successful
                - 403 FORBIDDEN if user is not a contributor
                - 400 BAD REQUEST if serializer validation fails
        Raises:
            Http404: If project or assigned user doesn't exist
        """
        project = get_object_or_404(CustomProject, id=project_id)
        if not Contributor.objects.filter(user=request.user, project=project).exists():
            return Response({"error": "You must be a contributor of the project to create an issue."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = IssueSerializer(data=request.data, context={'request': request, 'project': project})
        
        if serializer.is_valid():
            # The authenticated user becomes the author of the issue
            author_contributor = Contributor.objects.get(user=request.user, project=project)
            serializer.validated_data['author'] = author_contributor
            serializer.validated_data['project'] = project
            
            # Check if a specific contributor is assigned
            if 'user' in serializer.validated_data and serializer.validated_data['user']:
                assigned_contributor = serializer.validated_data['user']
                # Verify that the assigned contributor belongs to the project
                if assigned_contributor.project != project:
                    return Response({"error": "Assigned contributor must belong to this project."}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # If no contributor is assigned, leave the field empty (None)
            # The issue can remain unassigned
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request, project_id, issue_id):
        """
        Update an existing issue within a project.
        This method allows updating an issue if the requesting user is either:
        - The creator of the issue, or
        - The author of the project containing the issue
        Args:
            request: The HTTP request object containing the updated issue data
            project_id (int): The ID of the project containing the issue
            issue_id (int): The ID of the issue to update
        Returns:
            Response: 
                - 200: Updated issue data if successful
                - 400: Validation errors if the provided data is invalid
                - 403: Permission denied if user lacks modification rights
                - 404: If project or issue doesn't exist
        Raises:
            Http404: If the specified project or issue cannot be found
        """
        project = get_object_or_404(CustomProject, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)

        if request.user == issue.user.user or request.user == project.author:
            serializer = IssueSerializer(issue, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only the issue creator or project author can modify this issue."}, status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, project_id, issue_id):
        """
        Delete a specific issue from a project.
        This method allows the deletion of an issue by either the issue creator
        or the project author. Only authorized users can perform this operation.
        Args:
            request: The HTTP request object containing user authentication data.
            project_id (int): The unique identifier of the project containing the issue.
            issue_id (int): The unique identifier of the issue to be deleted.
        Returns:
            Response: HTTP 204 No Content on successful deletion.
            Response: HTTP 403 Forbidden if user lacks permission to delete the issue.
            Response: HTTP 404 Not Found if project or issue doesn't exist.
        Raises:
            Http404: When the specified project or issue is not found.
        Permissions:
            - Issue creator can delete their own issue
            - Project author can delete any issue within their project
        """
        project = get_object_or_404(CustomProject, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)
        
        if issue.user.user != request.user and project.author != request.user:
            return Response({"error": "Only the issue creator or project author can delete this issue."}, status=status.HTTP_403_FORBIDDEN)
        
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectCommentAPIView(APIView):
    """
    API view for managing comments within project issues.
    This view handles CRUD operations for comments that belong to specific issues within projects.
    All operations require authentication and proper comment permissions.
    
    Endpoints:
        GET /projects/{project_id}/issues/{issue_id}/comments/ - List all comments for an issue
        GET /projects/{project_id}/issues/{issue_id}/comments/{uuid}/ - Retrieve a specific comment
        POST /projects/{project_id}/issues/{issue_id}/comments/ - Create a new comment (contributors only)
        PUT /projects/{project_id}/issues/{issue_id}/comments/{uuid}/ - Update a comment (author only)
        DELETE /projects/{project_id}/issues/{issue_id}/comments/{uuid}/ - Delete a comment (author only)
    
    Permissions:
        - User must be authenticated
        - User must be a contributor of the project
        - POST: Any project contributor can create comments
        - PUT/DELETE: Only the comment author can modify/delete their comments
    """
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_object(self, project_id, issue_id, uuid=None):
        """
        Retrieve a project, issue, or comment object based on provided IDs.

        Args:
            project_id (int): The ID of the project containing the issue.
            issue_id (int): The ID of the issue containing the comment(s).
            uuid (UUID, optional): The UUID of the specific comment to retrieve.
                                  If None, returns all comments for the issue.
        Returns:
            Comment or QuerySet: 
                - If uuid is provided: Returns the specific Comment object
                - If uuid is None: Returns a QuerySet of all Comment objects for the issue
        Raises:
            Http404: If the project, issue, or comment with the given IDs doesn't exist.
        """
        project = get_object_or_404(CustomProject, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)
        
        if uuid:
            return get_object_or_404(Comment, uuid=uuid, issue=issue)
        else:
            return Comment.objects.filter(issue=issue)

    def get(self, request, project_id, issue_id, uuid=None):
        """
        Retrieve comment(s) for a specific issue within a project.
        
        Args:
            request: The HTTP request object
            project_id: ID of the project containing the issue
            issue_id: ID of the issue to retrieve comments from
            uuid (optional): UUID of a specific comment to retrieve
        Returns:
            Response: JSON response containing either:
                - Single comment data if uuid is provided
                - List of all comments for the issue if uuid is None
        Raises:
            Http404: If the project, issue, or comment does not exist
        """
        if uuid:
            comment = self.get_object(project_id, issue_id, uuid)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            comments = self.get_object(project_id, issue_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    def post(self, request, project_id, issue_id):
        """
        Create a new comment for a specific issue within a project.
        This endpoint allows contributors of a project to create new comments on issues.
        The user must be a contributor to the project to create a comment.
        
        Args:
            request: HTTP request object containing comment data
            project_id: ID of the project containing the issue
            issue_id: ID of the issue where the comment will be created
        Returns:
            Response: 
                - 201 CREATED with serialized comment data if successful
                - 403 FORBIDDEN if user is not a contributor
                - 400 BAD REQUEST if serializer validation fails
        Raises:
            Http404: If project or issue doesn't exist
        """
        project = get_object_or_404(CustomProject, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)
        
        if not Contributor.objects.filter(user=request.user, project=project).exists():
            return Response({"error": "You must be a contributor of the project to create a comment."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(data=request.data, context={'request': request, 'issue': issue})
        
        if serializer.is_valid():
            serializer.save(author=request.user, issue=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id, issue_id, uuid):
        """
        Update an existing comment within an issue.
        This method allows updating a comment only if the requesting user is the author of the comment.
        
        Args:
            request: The HTTP request object containing the updated comment data
            project_id (int): The ID of the project containing the issue
            issue_id (int): The ID of the issue containing the comment
            uuid (UUID): The UUID of the comment to update
        Returns:
            Response: 
                - 200: Updated comment data if successful
                - 400: Validation errors if the provided data is invalid
                - 403: Permission denied if user is not the comment author
                - 404: If project, issue, or comment doesn't exist
        Raises:
            Http404: If the specified project, issue, or comment cannot be found
        """
        comment = self.get_object(project_id, issue_id, uuid)

        if request.user != comment.author:
            return Response({"error": "Only the comment author can modify this comment."}, 
                          status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, uuid):
        """
        Delete a specific comment from an issue.
        This method allows the deletion of a comment only by the comment author.
        
        Args:
            request: The HTTP request object containing user authentication data.
            project_id (int): The unique identifier of the project containing the issue.
            issue_id (int): The unique identifier of the issue containing the comment.
            uuid (UUID): The unique identifier of the comment to be deleted.
        Returns:
            Response: HTTP 204 No Content on successful deletion.
            Response: HTTP 403 Forbidden if user is not the comment author.
            Response: HTTP 404 Not Found if project, issue, or comment doesn't exist.
        Raises:
            Http404: When the specified project, issue, or comment is not found.
        Permissions:
            - Only the comment author can delete their own comment
        """
        comment = self.get_object(project_id, issue_id, uuid)
        
        if comment.author != request.user:
            return Response({"error": "Only the comment author can delete this comment."}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)