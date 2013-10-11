# -*- coding=utf-8 -*-
from __future__ import print_function

import logging

import os.path
from os.path import dirname

from models import Post, Reply

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

NAMESPACE = os.path.basename(dirname(os.path.abspath(__file__)))

logger = logging.getLogger('debug')

@login_required
def home(request):
    user = request.user
    logger.debug('home()')
    posts = Post.objects.all()

    lst = []
    for post in posts:
        replies = Reply.objects.filter(post=post)
        logger.debug('replies: {}'.format(replies))
        logger.debug('id: {}'.format(post.id))
        lst.append({ 'post_id': post.id,
                     'post_theme': post.theme,
                     'replies': replies })

    return render(request, '{}/home.djhtml'.format(NAMESPACE),
                  { 'lst': lst })


def error(request):
    logger.debug('error()')
    return render(request, '{}/error.djhtml'.format(NAMESPACE))


@login_required
def motomeru(request):
    logger.debug('motomeru()')
    return render(request, '{}/motomeru.djhtml'.format(NAMESPACE))


@login_required
def send_motomeru_request(request):
    logger.debug('send_motomeru_motomeru()')
    theme = request.POST['theme']
    if not theme:
        logger.error('No theme provided')
        return redirect('tatoeru_core:error')

    if Post.objects.filter(theme=theme):
        logger.error('The exactly same theme already exists')
        return redirect('tatoeru_core:error')
               
    post = Post.objects.create(user=request.user,
                               theme=theme)
    logger.debug(post)
    return redirect('tatoeru_core:home')


@login_required
def kotaeru(request, post_id):
    logger.debug('kotaeru(): post_id={}'.format(post_id))

    lst = Post.objects.filter(id=post_id)
    if len(lst) < 1:
        logger.error('Unknown post_id {}'.format(post_id))
        return redirect('tatoeru_core:error')
    post = lst[0]

    return render(request, '{}/kotaeru.djhtml'.format(NAMESPACE),
                  { 'post_id': post.id,
                    'post_theme': post.theme })


@login_required
def send_kotaeru_request(request):
    user = request.user
    logger.debug('send_kotaeru_request()')
    post_id = request.POST['post_id']
    tatoe = request.POST['tatoe']

    lst = Post.objects.filter(id=post_id)
    if len(lst) < 1:
        logger.error('Unknown post_id {}'.format(post_id))
        return redirect('tatoeru_core:error')
    post = lst[0]

    reply = Reply.objects.create(user=request.user, post=post, tatoe=tatoe)
    logger.debug('reply={}'.format(reply))

    return redirect('tatoeru_core:home')
