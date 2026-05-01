import { useState, useMemo } from 'react';
import Fuse from 'fuse.js';

interface Post {
  slug: string;
  title: string;
  description: string;
  tags: string[];
  publishDate: string;
  href: string;
}

interface Props {
  posts: Post[];
}

export default function SearchBox({ posts }: Props) {
  const [query, setQuery] = useState('');

  const fuse = useMemo(
    () =>
      new Fuse(posts, {
        keys: ['title', 'description', 'tags'],
        threshold: 0.35,
        includeScore: true,
      }),
    [posts]
  );

  const results = query.trim()
    ? fuse.search(query).map((r) => r.item)
    : [];

  return (
    <div className="space-y-6">
      <div className="relative">
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted w-5 h-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>
        <input
          type="text"
          placeholder="포스트 검색..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
          className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/[0.06] border border-border-subtle
            text-text-primary placeholder-text-muted
            focus:outline-none focus:border-accent-amber/50 focus:bg-white/[0.08]
            transition-all duration-200"
        />
        {query && (
          <button
            onClick={() => setQuery('')}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary"
          >
            ✕
          </button>
        )}
      </div>

      {query.trim() && (
        <div>
          <p className="text-text-muted text-sm mb-4">
            "{query}"에 대한 검색 결과 {results.length}개
          </p>

          {results.length === 0 ? (
            <div className="glass-card p-10 text-center">
              <p className="text-text-muted">검색 결과가 없습니다.</p>
            </div>
          ) : (
            <ul className="space-y-3">
              {results.map((post) => (
                <li key={post.slug}>
                  <a
                    href={post.href}
                    className="glass-card p-5 block group"
                  >
                    <h3 className="font-semibold text-text-primary group-hover:text-accent-amber transition-colors duration-200 mb-1">
                      {post.title}
                    </h3>
                    <p className="text-text-secondary text-sm line-clamp-1">{post.description}</p>
                    <div className="flex gap-2 mt-2">
                      {post.tags.slice(0, 3).map((tag) => (
                        <span
                          key={tag}
                          className="text-xs text-text-muted bg-white/[0.05] px-2 py-0.5 rounded-full"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
