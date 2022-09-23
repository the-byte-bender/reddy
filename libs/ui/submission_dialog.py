import typing
from gi.repository import Gtk
import praw.models, praw.models.comment_forest
from .utils import LabeledTextbox, SimpleButton
from .reply_dialog import ReplyDialog
from .. import threadpool


class SubmissionDialog(Gtk.Dialog):
    def __init__(self, parrent: Gtk.Window, submission: praw.models.Submission):
        super().__init__(submission.title)
        self.submission = submission
        self.set_transient_for(parrent)
        self.content = self.get_content_area()
        self.box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.content.add(self.box)
        self.body = LabeledTextbox(
            submission.title, submission.selftext or submission.url or "", False, True
        )
        self.box.add(self.body)
        self.comments_store = Gtk.TreeStore(str, str, int, int, bool, bool, object)
        self.comments_label = Gtk.Label("Comments")
        self.comments_tree = Gtk.TreeView()
        self.comments_tree.get_accessible().set_name("Comments")
        self.box.add(self.comments_label)
        self.box.add(self.comments_tree)

        self.comment_body = LabeledTextbox("Comment body", "", False, True)
        self.box.add(self.comment_body)
        self.selection = self.comments_tree.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.BROWSE)
        self.selection.connect("changed", self.on_selection_change)
        self.text_renderer = Gtk.CellRendererText()
        self.upvote_toggle = Gtk.CellRendererToggle()
        self.upvote_toggle.connect("toggled", self.do_upvote)
        self.upvote_toggle.set_radio(True)
        self.downvote_toggle = Gtk.CellRendererToggle()
        self.downvote_toggle.connect("toggled", self.do_downvote)
        self.downvote_toggle.set_radio(True)
        self.comments_tree.set_model(self.comments_store)
        self.columns = [
            Gtk.TreeViewColumn("Author", self.text_renderer, text=0),
            Gtk.TreeViewColumn("Body preview", self.text_renderer, text=1),
            Gtk.TreeViewColumn("Upvotes", self.text_renderer, text=2),
            Gtk.TreeViewColumn("Replies", self.text_renderer, text=3),
            Gtk.TreeViewColumn("Upvote", self.upvote_toggle, active=4),
            Gtk.TreeViewColumn("Downvote", self.downvote_toggle, active=5),
        ]
        for column in self.columns:
            self.comments_tree.append_column(column)
        self.add_comments(None, submission.comments)
        self.add_action_widget(SimpleButton("_Comment...", self.comment), 0)
        self.add_action_widget(
            SimpleButton("_Reply to focused comment...", self.reply), 0
        )
        self.add_button("Close", Gtk.ResponseType.CLOSE)

    def add_comments(
        self,
        parrent: typing.Union[None, Gtk.TreeIter],
        comments: typing.Union[
            typing.Iterable[praw.models.Comment],
            praw.models.comment_forest.CommentForest,
        ],
        collapse_all: bool = True,
    ):
        for comment in comments:
            if isinstance(comment, praw.models.Comment):
                position = self.comments_store.append(
                    parrent,
                    [
                        comment.author.name,
                        comment.body
                        if len(comment.body) < 5000
                        else "Comment is too long to preview, please tab to view",
                        comment.score,
                        len(comment.replies),
                        comment.likes is True,
                        comment.likes is False,
                        comment,
                    ],
                )
                self.add_comments(position, comment.replies)
                if collapse_all:
                    self.comments_tree.collapse_all()

    def do_upvote(self, renderer, treepath):
        row = self.comments_store[treepath]
        upvote_value = row[4]
        comment = row[6]
        if not upvote_value:
            threadpool.submit(comment.upvote, None, threadpool=1)
            row[2] += 1
        else:
            threadpool.submit(comment.clear_vote, None, threadpool=1)
            row[2] -= 1
        row[4] = not upvote_value
        row[5] = False

    def do_downvote(self, renderer, treepath):
        row = self.comments_store[treepath]
        downvote_value = row[5]
        comment = row[6]
        if not downvote_value:
            threadpool.submit(comment.downvote, None, threadpool=1)
            row[2] -= 1
        else:
            threadpool.submit(comment.clear_vote, None, threadpool=1)
            row[2] += 1
        row[5] = not downvote_value
        row[4] = False

    def on_selection_change(self, selection):
        selection = self.comments_tree.get_selection()
        model, iter = selection.get_selected()
        if iter:
            comment = self.comments_store.get_value(iter, 6)
            self.comment_body.set_text(comment.body)

    def comment(self):
        if comment := ReplyDialog(
            self.get_toplevel(), "Write a comment", self.submission
        ).run():
            self.add_comments(None, [comment])

    def reply(self):
        selection = self.comments_tree.get_selection()
        model, iter = selection.get_selected()
        parent_comment = self.comments_store.get_value(iter, 6)
        comment = ReplyDialog(
            self.get_toplevel(), "Write a reply", parent_comment
        ).run()
        if comment is not None:
            print("\a")
            self.add_comments(iter, [comment])
